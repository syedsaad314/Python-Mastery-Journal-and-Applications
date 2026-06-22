"""
Core Topic: Binary Indexed Tree (Fenwick Tree) Ledger
Description: Harnessing low-bit integer math manipulations to track running prefix sums.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class BinaryIndexedTree:
    def __init__(self, size: int):
        self.size = size
        # Fenwick trees utilize 1-based indexing frameworks internally
        self.tree = [0] * (self.size + 1)

    def update_delta(self, index: int, delta: int) -> None:
        """Propagates delta value modifications upward through the bit sequence paths."""
        index += 1  # Shift up to align with 1-based internal array indexing
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index)  # Isolate and add the lowest set bit

    def query_prefix_sum(self, index: int) -> int:
        """Calculates running accumulations from the root down to the target index."""
        index += 1
        running_sum = 0
        while index > 0:
            running_sum += self.tree[index]
            index -= index & (-index)  # Isolate and subtract the lowest set bit
        return running_sum

if __name__ == "__main__":
    ledger = BinaryIndexedTree(6)
    
    # Simulating data ingestion events by applying changes at specific indices
    ledger.update_delta(index=1, delta=10)
    ledger.update_delta(index=2, delta=5)
    ledger.update_delta(index=3, delta=20)
    
    print(f"Prefix Sum Total for Upper Bounds [0-3]: {ledger.query_prefix_sum(3)}")