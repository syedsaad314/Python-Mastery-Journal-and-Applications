"""
Core Topic: Segment Tree with Lazy Propagation
Description: defers group updates by caching changes inside a lazy tracking array.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import List

class LazySegmentTree:
    def __init__(self, data: List[int]) -> None:
        self.n: int = len(data)
        self.raw_data: List[int] = data
        self.tree: List[int] = [0] * (4 * self.n)
        self.lazy: List[int] = [0] * (4 * self.n)
        if self.n > 0:
            self._build(0, 0, self.n - 1)

    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = self.raw_data[start]
            return
        mid = (start + end) // 2
        self._build(2 * node + 1, start, mid)
        self._build(2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def _push_pending_updates(self, node: int, start: int, end: int) -> None:
        """Pushes a cached update down to a node's children when a path is actively accessed."""
        if self.lazy[node] != 0:
            value_to_add = self.lazy[node]
            # Apply the cached changes to the current node's total range sum
            self.tree[node] += (end - start + 1) * value_to_add
            
            # If the node has children, pass the lazy update down to them
            if start != end:
                self.lazy[2 * node + 1] += value_to_add
                self.lazy[2 * node + 2] += value_to_add
                
            # Clear the lazy flag for the current node
            self.lazy[node] = 0

    def _update_range(self, node: int, start: int, end: int, left: int, right: int, val: int) -> None:
        # Resolve any existing lazy updates before processing this node
        self._push_pending_updates(node, start, end)
        
        # No overlap condition
        if start > end or start > right or end < left:
            return
            
        # Complete overlap condition
        if left <= start and end <= right:
            self.tree[node] += (end - start + 1) * val
            if start != end:
                self.lazy[2 * node + 1] += val
                self.lazy[2 * node + 2] += val
            return
            
        # Partial overlap condition
        mid = (start + end) // 2
        self._update_range(2 * node + 1, start, mid, left, right, val)
        self._update_range(2 * node + 2, mid + 1, end, left, right, val)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def _query_range(self, node: int, start: int, end: int, left: int, right: int) -> int:
        self._push_pending_updates(node, start, end)
        
        if start > end or start > right or end < left:
            return 0
            
        if left <= start and end <= right:
            return self.tree[node]
            
        mid = (start + end) // 2
        return (self._query_range(2 * node + 1, start, mid, left, right) + 
                self._query_range(2 * node + 2, mid + 1, end, left, right))

    def update_range(self, left: int, right: int, value: int) -> None:
        self._update_range(0, 0, self.n - 1, left, right, value)

    def query_range_sum(self, left: int, right: int) -> int:
        return self._query_range(0, 0, self.n - 1, left, right)


if __name__ == "__main__":
    array = [1, 2, 3, 4, 5]
    lazy_tree = LazySegmentTree(array)
    
    # Add value 5 to all indices from 1 to 3 -> array becomes [1, 7, 8, 9, 5]
    lazy_tree.update_range(left=1, right=3, value=5)
    print("[RANGE UPDATE] Added value 5 to indices [1, 3]")
    
    # Query sum of range [1, 4] -> 7 + 8 + 9 + 5 = 29
    print(f"Sum of range [1, 4]: {lazy_tree.query_range_sum(1, 4)}")