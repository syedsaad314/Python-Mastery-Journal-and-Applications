"""
Core Topic: Standard Segment Tree Structure
Description: Balanced binary tree structure managing dynamic array range sum lookups and individual point updates.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import List

class SegmentTree:
    def __init__(self, data: List[int]) -> None:
        self.n: int = len(data)
        self.raw_data: List[int] = data
        # Allocate space for tree nodes (4 * N ensures safe array bounds)
        self.tree: List[int] = [0] * (4 * self.n)
        if self.n > 0:
            self._build(0, 0, self.n - 1)

    def _build(self, node: int, start: int, end: int) -> None:
        """Constructs the segment tree nodes recursively from the bottom up."""
        if start == end:
            self.tree[node] = self.raw_data[start]
            return
            
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        self._build(left_child, start, mid)
        self._build(right_child, mid + 1, end)
        
        # Internal node stores the combined sum of its children
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def _query(self, node: int, start: int, end: int, left: int, right: int) -> int:
        """Queries an interval range sum by traversing relevant sub-trees."""
        # No overlap condition
        if right < start or end < left:
            return 0
            
        # Complete overlap condition
        if left <= start and end <= right:
            return self.tree[node]
            
        # Partial overlap condition: branch down to evaluate both paths
        mid = (start + end) // 2
        return (self._query(2 * node + 1, start, mid, left, right) + 
                self._query(2 * node + 2, mid + 1, end, left, right))

    def _update(self, node: int, start: int, end: int, index: int, value: int) -> None:
        """Traverses downward to modify a leaf element, then updates parent sums on the way back up."""
        if start == end:
            self.tree[node] = value
            return
            
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        if start <= index <= mid:
            self._update(left_child, start, mid, index, value)
        else:
            self._update(right_child, mid + 1, end, index, value)
            
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def query_sum(self, left: int, right: int) -> int:
        return self._query(0, 0, self.n - 1, left, right)

    def update_point(self, index: int, value: int) -> None:
        self._update(0, 0, self.n - 1, index, value)


if __name__ == "__main__":
    elements = [1, 3, 5, 7, 9, 11]
    seg_tree = SegmentTree(elements)
    
    print(f"Initial sum of range [1, 3]: {seg_tree.query_sum(1, 3)}") # 3 + 5 + 7 = 15
    
    # Modify index 1 from value 3 to value 10
    seg_tree.update_point(index=1, value=10)
    print("[UPDATE] Modified index 1 to value 10")
    
    print(f"Updated sum of range [1, 3]: {seg_tree.query_sum(1, 3)}") # 10 + 5 + 7 = 22