"""
Core Topic: Mo's Algorithm (Offline Range Query Optimization)
Description: Sorts and groups ranges by square-root block boundaries to minimize pointer travel.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import math
from typing import List, Tuple

class MosAlgorithm:
    def __init__(self, data: List[int]) -> None:
        self.raw_data: List[int] = data
        self.block_size: int = int(math.isqrt(len(data))) if data else 1

    def process_queries(self, queries: List[Tuple[int, int]]) -> List[int]:
        """Sorts and executes all range queries offline to minimize index pointer movement."""
        # Store queries alongside their original indices to ensure results match the requested order
        indexed_queries = [(q[0], q[1], idx) for idx, q in enumerate(queries)]
        
        # Sort queries: first by their square-root block index, then by their right boundary
        indexed_queries.sort(key=lambda x: (x[0] // self.block_size, x[1]))
        
        results = [0] * len(queries)
        
        # Tracking states for pointer locations and the running total
        current_left = 0
        current_right = -1
        running_sum = 0

        for L, R, original_idx in indexed_queries:
            # Expand the right boundary forward
            while current_right < R:
                current_right += 1
                running_sum += self.raw_data[current_right]
                
            # Expand the left boundary backward
            while current_left > L:
                current_left -= 1
                running_sum += self.raw_data[current_left]
                
            # Contract the right boundary backward
            while current_right > R:
                running_sum -= self.raw_data[current_right]
                current_right -= 1
                
            # Contract the left boundary forward
            while current_left < L:
                running_sum -= self.raw_data[current_left]
                current_left += 1
                
            results[original_idx] = running_sum
            
        return results


if __name__ == "__main__":
    array = [1, 3, 2, 4, 1, 0, 5]
    # Collection of ranges to evaluate: [0,4], [1,3], [2,6]
    search_queries = [(0, 4), (1, 3), (2, 6)]
    
    mo_engine = MosAlgorithm(array)
    outcomes = mo_engine.process_queries(search_queries)
    print(f"Calculated offline query range answers: {outcomes}")