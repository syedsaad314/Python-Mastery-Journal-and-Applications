"""
Core Topic: Square Root (Sqrt) Decomposition
Description: Segments an array into square-root-sized blocks to balance query speeds and update times.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import math
from typing import List

class SqrtDecomposition:
    def __init__(self, data: List[int]) -> None:
        self.raw_data: List[int] = data
        self.n: int = len(data)
        
        # Calculate block length size limits (~ sqrt(N))
        self.block_size: int = int(math.isqrt(self.n)) if self.n > 0 else 1
        num_blocks = (self.n + self.block_size - 1) // self.block_size
        
        # Initialize block tracking totals
        self.blocks: List[int] = [0] * num_blocks
        
        # Populate initial values into block buckets
        for i in range(self.n):
            block_idx = i // self.block_size
            self.blocks[block_idx] += data[i]

    def update_point(self, index: int, new_value: int) -> None:
        """Updates a single element and adjusts its corresponding block total in constant O(1) time."""
        if index < 0 or index >= self.n:
            raise IndexError("Index out of array boundaries.")
            
        block_idx = index // self.block_size
        # Adjust block total by calculating the difference
        delta = new_value - self.raw_data[index]
        self.blocks[block_idx] += delta
        self.raw_data[index] = new_value

    def query_range_sum(self, left: int, right: int) -> int:
        """Queries range sums in O(sqrt(N)) time by combining full blocks and partial boundaries."""
        if left > right or left < 0 or right >= self.n:
            return 0
            
        total_sum = 0
        start_block = left // self.block_size
        end_block = right // self.block_size
        
        # Condition A: Query falls within the same block bucket
        if start_block == end_block:
            for i in range(left, right + 1):
                total_sum += self.raw_data[i]
            return total_sum
            
        # Condition B: Query spans across multiple blocks
        # 1. Add trailing elements from the partial starting block
        end_of_first_block = (start_block + 1) * self.block_size
        for i in range(left, end_of_first_block):
            total_sum += self.raw_data[i]
            
        # 2. Add precalculated totals from full intermediate blocks
        for b in range(start_block + 1, end_block):
            total_sum += self.blocks[b]
            
        # 3. Add leading elements from the partial ending block
        start_of_last_block = end_block * self.block_size
        for i in range(start_of_last_block, right + 1):
            total_sum += self.raw_data[i]
            
        return total_sum


if __name__ == "__main__":
    elements = [1, 5, 2, 4, 6, 1, 3, 5, 7, 10]
    decom_engine = SqrtDecomposition(elements)
    
    print(f"Sum of range [1, 7]: {decom_engine.query_range_sum(1, 7)}") # 5+2+4+6+1+3+5 = 26
    
    # Modify index 3 from value 4 to value 20
    decom_engine.update_point(index=3, new_value=20)
    print("[UPDATE] Changed index 3 value to 20")
    
    print(f"New sum of range [1, 7]: {decom_engine.query_range_sum(1, 7)}") # 5+2+20+6+1+3+5 = 42