"""
Core Topic: Kruskal's Minimum Spanning Tree (MST)
Description: Edge-centric sorting combined with Disjoint Set Union tracking to establish light frameworks.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class FastUnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])  # Path compression injection
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Union strategy optimized by tracking sub-tree rank sizes
            if self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            elif self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

class KruskalsMSTEngine:
    @staticmethod
    def compute_mst(total_nodes: int, edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
        """Assembles a clear Minimum Spanning Tree backbone by filtering globally sorted edges."""
        # Sort edges by weight to enable global greedy processing
        sorted_edges = sorted(edges, key=lambda edge: edge[2])
        union_find = FastUnionFind(total_nodes)
        minimum_spanning_tree = []

        for u, v, weight in sorted_edges:
            # If nodes are in different groups, merge them to safely add the edge without creating a cycle
            if union_find.union(u, v):
                minimum_spanning_tree.append((u, v, weight))
                if len(minimum_spanning_tree) == total_nodes - 1:
                    break  # Tree structure complete

        return minimum_spanning_tree

if __name__ == "__main__":
    # Edge record schema: (source_node, target_node, weight)
    graph_edge_pool = [
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4)
    ]
    
    mst_result = KruskalsMSTEngine.compute_mst(total_nodes=4, edges=graph_edge_pool)
    print(f"Isolated Kruskal's MST Backbone Edge Connections List: {mst_result}")