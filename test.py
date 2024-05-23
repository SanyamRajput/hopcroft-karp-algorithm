from collections import deque, defaultdict

class BipartiteGraph:
    def __init__(self, left, right):
        self.graph = defaultdict(list)
        self.left = left
        self.right = right
        self.pair_u = {}
        self.pair_v = {}
        self.dist = {}

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

        # print(self.graph)
        print(f'{u}->{v}', end='\t')

    def bfs(self):
        queue = deque()
        for u in self.left:
            if self.pair_u[u] is None:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float('inf')

        self.dist[None] = float('inf')

        while queue:
            u = queue.popleft()
            if self.dist[u] < self.dist[None]:
                for v in self.graph[u]:
                    if self.dist[self.pair_v[v]] == float('inf'):
                        self.dist[self.pair_v[v]] = self.dist[u] + 1
                        queue.append(self.pair_v[v])

        return self.dist[None] != float('inf')

    def dfs(self, u):
        if u is not None:
            for v in self.graph[u]:
                if self.dist[self.pair_v[v]] == self.dist[u] + 1:
                    if self.dfs(self.pair_v[v]):
                        self.pair_v[v] = u
                        self.pair_u[u] = v
                        return True
            self.dist[u] = float('inf')
            return False
        return True

    def hopcroft_karp(self):
        self.pair_u = {u: None for u in self.left}
        self.pair_v = {v: None for v in self.right}
        self.dist = {}
        matching = 0

        while self.bfs():
            for u in self.left:
                if self.pair_u[u] is None:
                    if self.dfs(u):
                        matching += 1

        matching_pairs = [(u, v) for u, v in self.pair_u.items() if v is not None]
        return matching, matching_pairs

    def print_edges(self):
        for u in self.left:
            for v in self.graph[u]:
                print(f"Edge from {u} to {v}")

# Define the bipartite graph
left = {'a', 'b', 'c', 'd', 'e'}
right = {'A', 'B', 'C', 'D'}

bg = BipartiteGraph(left, right)

edges = {
    ('a', 'A'), ('a', 'C'),
    ('b', 'A'), ('b', 'B'), ('b', 'C'),
    ('c', 'B'), ('c', 'C'),
    ('d', 'B'), ('d', 'C'), ('d', 'D'),
    ('e', 'A'), ('e', 'C'), ('e', 'D')
}

# print(edges)
# edgeArr = list(edges)
# edgeArr.sort()
# edges = set(edges)

for u, v in edges:
    bg.add_edge(u, v)

# Print all edges
# print("Edges:")
# bg.print_edges()

# Compute maximum matching using Hopcroft-Karp algorithm
matching_size, matching_pairs = bg.hopcroft_karp()
print(f"\nThe maximum possible matching is {matching_size}")
print(f"The matching pairs are: {matching_pairs}")
