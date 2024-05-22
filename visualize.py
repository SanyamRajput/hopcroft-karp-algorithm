import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

# Define the bipartite graph
graph = {
    'U': ['a', 'b', 'c', 'd', 'e'],  # U set
    'V': ['A', 'B', 'C', 'D'],  # V set
    'edges': {
        'a': ['A', 'C'],
        'b': ['B', 'C', 'D'],
        'c': ['A', 'B', 'C'], 
        'd': ['C', 'D'], 
        'e': ['A', 'C', 'D']
    }
}

# BFS for Hopcroft-Karp algorithm
def bfs(graph, pair_U, pair_V, dist):
    queue = deque()
    for u in graph['U']:
        if pair_U[u] is None:
            dist[u] = 0
            queue.append(u)
        else:
            dist[u] = float('inf')
    
    dist[None] = float('inf')
    
    while queue:
        u = queue.popleft()
        if dist[u] < dist[None]:
            for v in graph['edges'][u]:
                if dist[pair_V[v]] == float('inf'):
                    dist[pair_V[v]] = dist[u] + 1
                    queue.append(pair_V[v])
    
    return dist[None] != float('inf')

# DFS for Hopcroft-Karp algorithm
def dfs(graph, u, pair_U, pair_V, dist):
    if u is not None:
        for v in graph['edges'][u]:
            if dist[pair_V[v]] == dist[u] + 1:
                if dfs(graph, pair_V[v], pair_U, pair_V, dist):
                    pair_V[v] = u
                    pair_U[u] = v
                    return True
        dist[u] = float('inf')
        return False
    return True

# Hopcroft-Karp algorithm
def hopcroft_karp(graph):
    pair_U = {u: None for u in graph['U']}
    pair_V = {v: None for v in graph['V']}
    dist = {}

    matching = 0
    
    while bfs(graph, pair_U, pair_V, dist):
        for u in graph['U']:
            if pair_U[u] is None:
                if dfs(graph, u, pair_U, pair_V, dist):
                    matching += 1

    return matching, pair_U, pair_V

# Visualize the bipartite graph with matching
def visualize_matching(graph, pair_U, pair_V):
    B = nx.Graph()
    B.add_nodes_from(graph['U'], bipartite=0)
    B.add_nodes_from(graph['V'], bipartite=1)
    
    for u in graph['edges']:
        for v in graph['edges'][u]:
            B.add_edge(u, v)
    
    pos = {node: (0, i) for i, node in enumerate(graph['U'])}
    pos.update({node: (1, i) for i, node in enumerate(graph['V'])})
    
    # Draw the bipartite graph
    plt.figure(figsize=(8, 6))
    nx.draw(B, pos, with_labels=True, node_color=['lightblue' if node in graph['U'] else 'lightgreen' for node in B.nodes])
    
    # Highlight the matching edges
    matching_edges = [(u, pair_U[u]) for u in pair_U if pair_U[u] is not None]
    nx.draw_networkx_edges(B, pos, edgelist=matching_edges, edge_color='r', width=2)
    
    plt.title("Bipartite Graph with Maximum Matching")
    plt.show()

# Execute the Hopcroft-Karp algorithm
matching, pair_U, pair_V = hopcroft_karp(graph)

# Visualize the matching
visualize_matching(graph, pair_U, pair_V)
