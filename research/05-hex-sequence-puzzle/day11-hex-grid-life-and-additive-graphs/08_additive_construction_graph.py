# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/08_additive_construction_graph.py
# Original location      :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/8.py   (last edited 2025-08-12)
# What this script does  :: Integer partitions as an additive construction graph with Dijkstra paths.
# ----------------------------------------------------------------------------
import networkx as nx
import matplotlib.pyplot as plt
import heapq
from collections import defaultdict

# Integer partitioning: for each number up to n, generate all additive decompositions
def generate_partitions(n):
    # Helper function for recursive partitioning
    def partitions(num, max_part):
        if num == 0:
            return [[]]
        result = []
        for i in range(1, min(num, max_part) + 1):
            for tail in partitions(num - i, i):
                result.append([i] + tail)
        return result

    all_partitions = {}
    for k in range(1, n + 1):
        all_partitions[k] = partitions(k, k)
    return all_partitions


# Build a directed graph where each node is a number, and edges represent additive construction
def build_additive_graph(n):
    G = nx.DiGraph()
    G.add_nodes_from(range(1, n+1))
    for num in range(2, n+1):
        for i in range(1, num):
            if num - i >= 1:
                G.add_edge(i, num)
    return G


def draw_graph(G):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', arrowsize=20, font_size=10)
    plt.title("Additive Construction Graph")
    plt.show()

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

def find_shortest_path_to_number(n, target_number):
    """
    Find shortest path from 1 to target_number in the additive construction graph.
    """
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
    """
    Print detailed analysis of the path.
    """
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

# Example usage
if __name__ == "__main__":
    n = 50  # Change this value as needed
    blocks = generate_partitions(n)
    for num in range(1, n + 1):
        print(f"{num}: {blocks[num]}")

    # Build and draw the additive graph
    G = build_additive_graph(n)
    draw_graph(G)
    
    # Test Dijkstra's algorithm
    target = 25  # Change this to test different targets
    print(f"\nFinding shortest path to {target}...")
    distance, path = find_shortest_path_to_number(n, target)
    print_path_analysis(distance, path)

