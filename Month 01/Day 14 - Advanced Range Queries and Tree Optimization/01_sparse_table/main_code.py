"""
Core Topic: Sparse Table Structure (Static Range Minimum Query)
Description: Precomputes power-of-two range states to yield O(1) immutable interval queries.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import math
from typing import List

class SparseTable:
    def __init__(self, data: List[int]) -> None:
        self.n: int = len(data)
        if self.n == 0:
            return
        
        # Max power of 2 that fits within array size
        self.max_power: int = int(math.log2(self.n)) + 1
        # Allocate matrix lookup table shape: [N][max_power]
        self.table: List[List[int]] = [[0] * self.max_power for _ in range(self.n)]
        
        # Base cases: intervals of length 2^0 = 1
        for i in range(self.n):
            self.table[i][0] = data[i]
            
        # Compute range values using dynamic programming transitions
        for j in range(1, self.max_power):
            i = 0
            while i + (1 << j) <= self.n:
                # Minimum of left half and right half components
                self.table[i][j] = min(
                    self.table[i][j - 1], 
                    self.table[i + (1 << (j - 1))][j - 1]
                )
                i += 1

    def query_min(self, left: int, right: int) -> int:
        """Returns the minimum value within the [left, right] range in continuous O(1) time."""
        if left > right or left < 0 or right >= self.n:
            raise ValueError("Invalid query boundaries.")
            
        length = right - left + 1
        k = int(math.log2(length))
        
        # Overlap two power-of-two ranges to completely span the requested range
        return min(self.table[left][k], self.table[right - (1 << k) + 1][k])


if __name__ == "__main__":
    array = [7, 2, 3, 0, 5, 10, 3, 12, 18]
    sparse_table = SparseTable(array)
    
    print(f"Minimum in range [0, 4]: {sparse_table.query_min(0, 4)}")  # 0
    print(f"Minimum in range [4, 7]: {sparse_table.query_min(4, 7)}")  # 3
    print(f"Minimum in range [1, 2]: {sparse_table.query_min(1, 2)}")  # 2