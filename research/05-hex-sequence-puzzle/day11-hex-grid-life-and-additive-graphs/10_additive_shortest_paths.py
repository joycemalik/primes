# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/10_additive_shortest_paths.py
# Original location      :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/test_complex_path.py   (last edited 2025-08-13)
# What this script does  :: Shortest additive construction paths with alternatives.
# ----------------------------------------------------------------------------
import networkx as nx
import heapq

def dijkstra_shortest_path(G, start, target):
    """Find shortest path from start to target using Dijkstra's algorithm."""
    if start == target:
        return 0, [start]
    
    pq = [(0, start, [start])]
    visited = set()
    
    while pq:
        dist, current, path = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)
        
        if current == target:
            return dist, path
        
        for neighbor in G.successors(current):
            if neighbor not in visited:
                new_dist = dist + 1
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_dist, neighbor, new_path))
    
    return float('inf'), []

def build_additive_graph(n):
    """Build a directed graph where each node is a number, and edges represent additive construction"""
    G = nx.DiGraph()
    G.add_nodes_from(range(1, n+1))
    for num in range(2, n+1):
        for i in range(1, num):
            if num - i >= 1:
                G.add_edge(i, num)
    return G

def find_shortest_path_to_number(n, target_number):
    """Find shortest path from 1 to target_number in the additive construction graph."""
    if target_number > n:
        print(f"Target number {target_number} is greater than graph size {n}")
        return None, None
    
    G = build_additive_graph(n)
    
    if not nx.has_path(G, 1, target_number):
        print(f"No path exists from 1 to {target_number}")
        return None, None
    
    distance, path = dijkstra_shortest_path(G, 1, target_number)
    return distance, path

def print_path_analysis(distance, path):
    """Print detailed analysis of the path."""
    if distance is None:
        return
    
    print(f"Distance: {distance} steps")
    print(f"Path: {' -> '.join(map(str, path))}")
    print(f"Step-by-step construction:")
    
    for i in range(1, len(path)):
        prev = path[i-1]
        curr = path[i]
        print(f"  Step {i}: {prev} + {curr - prev} = {curr}")

# Test with more interesting cases
if __name__ == "__main__":
    print("Testing Dijkstra's algorithm with more complex scenarios")
    print("=" * 60)
    
    # Test cases that might have multiple possible paths
    test_cases = [7, 12, 18, 30]
    
    for target in test_cases:
        print(f"\nFinding shortest path to {target}...")
        distance, path = find_shortest_path_to_number(50, target)
        print_path_analysis(distance, path)
        
        # Show alternative paths (if any)
        G = build_additive_graph(50)
        all_paths = list(nx.all_simple_paths(G, 1, target))
        if len(all_paths) > 1:
            print(f"Note: There are {len(all_paths)} different paths from 1 to {target}")
            print("Alternative paths:")
            for i, alt_path in enumerate(all_paths[1:3], 2):  # Show first 2 alternatives
                print(f"  Path {i}: {' -> '.join(map(str, alt_path))} (length: {len(alt_path)-1})")

