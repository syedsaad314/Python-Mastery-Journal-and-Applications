"""
Core Topic: Disjoint Set Union (DSU / Union-Find)
Description: High-performance partition structure with path compression and rank-based optimizations.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class DisjointSetUnion:
    def __init__(self, elements_count: int):
        # Every node starts as its own independent root parent
        self.parent = list(range(elements_count))
        self.rank = [0] * elements_count

    def find(self, element: int) -> int:
        """Finds the root representative of a group, using path compression for flat lookups."""
        if self.parent[element] != element:
            # Flatten the tree structure dynamically by pointing directly to the root
            self.parent[element] = self.find(self.parent[element])
        return self.parent[element]

    def union_sets(self, first_element: int, second_element: int) -> bool:
        """Merges two independent sets based on their tree rank size to maintain balance."""
        root_x = self.find(first_element)
        root_y = self.find(second_element)

        if root_x == root_y:
            return False  # Already in the same group (merging would create a cycle)

        # Attach the shallower tree under the deeper tree to keep height minimal
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

if __name__ == "__main__":
    # Modeling independent asset groupings
    dsu_cluster = DisjointSetUnion(elements_count=5)
    
    print(f"Initial Group Connections: Node [1] and [2] merged -> {dsu_cluster.union_sets(1, 2)}")
    print(f"Subsequent Group Connections: Node [3] and [4] merged -> {dsu_cluster.union_sets(3, 4)}")
    print(f"Cross-Cluster Connections: Node [2] and [4] merged -> {dsu_cluster.union_sets(2, 4)}")
    
    # Check if node 1 and node 3 are now in the same group
    same_partition = dsu_cluster.find(1) == dsu_cluster.find(3)
    print(f"Verification: Are Node [1] and Node [3] linked in the same group? -> {same_partition}")