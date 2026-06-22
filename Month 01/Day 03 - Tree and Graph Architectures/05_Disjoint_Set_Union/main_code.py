"""
CORE CONCEPT: Disjoint Set Union (DSU / Union-Find) Data Structure
Implementing a highly optimized partition engine utilizing iterative path compression 
and ranking analytics. Tracks element clustering groups efficiently from raw principles.
"""

class DisjointSetUnion:
    def __init__(self, element_count: int):
        # Set every isolated element as its own structural cluster root parent
        self.parent_array: list[int] = list(range(element_count))
        # Rank array tracking directional depth profiles to balance tree mergers
        self.rank_array: list[int] = [0] * element_count

    def find_representative(self, element: int) -> int:
        """Finds the root representative of a set, applying path compression along the way."""
        if self.parent_array[element] != element:
            # Flatten paths recursively by pointing nodes directly to the master cluster root
            self.parent_array[element] = self.find_representative(self.parent_array[element])
        return self.parent_array[element]

    def union_sets(self, element_a: int, element_b: int) -> bool:
        """Merges two independent sets based on their tree rank, returning True if a merge occurs."""
        root_a = self.find_representative(element_a)
        root_b = self.find_representative(element_b)

        if root_a == root_b:
            return False  # Elements already share the same cluster path partition

        # Balance trees by linking the lower rank structure beneath the higher rank root
        if self.rank_array[root_a] < self.rank_array[root_b]:
            self.parent_array[root_a] = root_b
        elif self.rank_array[root_a] > self.rank_array[root_b]:
            self.parent_array[root_b] = root_a
        else:
            self.parent_array[root_b] = root_a
            self.rank_array[root_a] += 1

        return True


if __name__ == "__main__":
    # Initialize DSU tracking 5 independent network coordinates
    dsu = DisjointSetUnion(element_count=5)
    
    # Merge groups together: Cluster (0,1) and Cluster (2,3)
    dsu.union_sets(0, 1)
    dsu.union_sets(2, 3)
    
    print(f"Are Node 0 and Node 1 in the same set? -> {dsu.find_representative(0) == dsu.find_representative(1)}")
    print(f"Are Node 1 and Node 2 in the same set? -> {dsu.find_representative(1) == dsu.find_representative(2)}")
    
    # Connect separate clusters together
    dsu.union_sets(1, 2)
    print(f"Post-Union: Are Node 1 and Node 2 in the same set? -> {dsu.find_representative(1) == dsu.find_representative(2)}")