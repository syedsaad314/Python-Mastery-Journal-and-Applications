"""
Core Topic: Fenwick Tree (Binary Indexed Tree)
Description: Memory-optimized tree structure using bitwise operations to compute running prefix sums.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import List

class FenwickTree:
    def __init__(self, size: int) -> None:
        self.size: int = size
        # 1-indexed internal flat array representation
        self.tree: List[int] = [0] * (size + 1)

    def update(self, index: int, delta: int) -> None:
        """Adds a value change to the specified index and updates affected upper-level prefix sums."""
        # Convert index to 1-based format internally
        i = index + 1
        while i <= self.size:
            self.tree[i] += delta
            # Isolate the lowest set bit and step forward
            i += (i & -i)

    def query_prefix_sum(self, index: int) -> int:
        """Computes the cumulative sum from the start of the array up to the given index."""
        i = index + 1
        total_sum = 0
        while i > 0:
            total_sum += self.tree[i]
            # Strip the lowest set bit to jump backward across precalculated intervals
            i -= (i & -i)
        return total_sum

    def query_range(self, left: int, right: int) -> int:
        """Calculates the sum over an interval [left, right] using prefix sum differences."""
        if left > right:
            return 0
        if left == 0:
            return self.query_prefix_sum(right)
        return self.query_prefix_sum(right) - self.query_prefix_sum(left - 1)


if __name__ == "__main__":
    data_source = [2, 4, 1, 3, 8, 5]
    bit = FenwickTree(len(data_source))
    
    # Initialize tree elements sequentially
    for idx, val in enumerate(data_source):
        bit.update(idx, val)
        
    print(f"Prefix sum up to index 3: {bit.query_prefix_sum(3)}")  # 2 + 4 + 1 + 3 = 10
    print(f"Sum over interval range [2, 4]: {bit.query_range(2, 4)}") # 1 + 3 + 8 = 12
    
    # Apply an update: increment index 2 by value 5 (value 1 becomes 6)
    bit.update(index=2, delta=5)
    print("[UPDATE] Incremented value at index 2 by 5")
    print(f"New sum over interval range [2, 4]: {bit.query_range(2, 4)}") # 6 + 3 + 8 = 17