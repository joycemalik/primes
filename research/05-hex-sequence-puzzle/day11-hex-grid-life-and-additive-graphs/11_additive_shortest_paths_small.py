# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/11_additive_shortest_paths_small.py
# Original location      :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/test_dijkstra.py   (last edited 2025-08-12)
# What this script does  :: The same Dijkstra test on smaller numbers.
# ----------------------------------------------------------------------------
import networkx as nx
import heapq

def dijkstra_shortest_path(G, start, target):
    """
    Find shortest path from start to target using Dijkstra's algorithm.
    Returns (distance, path) where path is a list of nodes.
    """
    if start == target:
        return 0, [start]
    
    # Priority queue: (distance, current_node, path)
    pq = [(0, start, [start])]
    visited = set()
    
    while pq:
        dist, current, path = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)
        
        if current == target:
            return dist, path
        
        # Explore neighbors
        for neighbor in G.successors(current):
            if neighbor not in visited:
                new_dist = dist + 1  # All edges have weight 1
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_dist, neighbor, new_path))
    
    return float('inf'), []  # No path found

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
    
    # Check if target is reachable
    if not nx.has_path(G, 1, target_number):
        print(f"No path exists from 1 to {target_number}")
        return None, None
    
    distance, path = dijkstra_shortest_path(G, 1, target_number)
    return distance, path

def print_path_analysis(distance, path):
    """Print detailed analysis of the path."""
    if distance is None:
        return
    
    print(f"\nShortest path analysis:")
    print(f"Distance: {distance} steps")
    print(f"Path: {' -> '.join(map(str, path))}")
    print(f"\nStep-by-step construction:")
    
    for i in range(1, len(path)):
        prev = path[i-1]
        curr = path[i]
        print(f"  Step {i}: {prev} + {curr - prev} = {curr}")

# Test with smaller numbers
if __name__ == "__main__":
    print("Testing Dijkstra's algorithm for additive construction graph")
    print("=" * 60)
    
    # Test cases
    test_cases = [5, 10, 15, 20, 25]
    
    for target in test_cases:
        print(f"\nFinding shortest path to {target}...")
        distance, path = find_shortest_path_to_number(50, target)
        print_path_analysis(distance, path)
