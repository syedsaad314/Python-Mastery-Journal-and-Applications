"""
CORE CONCEPT: Compressed Sparse Row (CSR) Matrix Engine
Implementing a low-level vector compression structure that eliminates non-zero values 
from large multi-dimensional matrices. Replaces a dense representation with three 
one-dimensional tracking arrays: Values, Column Indices, and Row Pointers.
"""

class CompressedSparseRowMatrix:
    def __init__(self, dense_matrix: list[list[float]]):
        if not dense_matrix or not dense_matrix[0]:
            raise ValueError("Input matrix must possess non-empty dimensions.")
            
        self.num_rows = len(dense_matrix)
        self.num_cols = len(dense_matrix[0])
        
        self.values = []
        self.col_indices = []
        self.row_pointers = [0]
        
        self._compress(dense_matrix)

    def _compress(self, dense_matrix: list[list[float]]) -> None:
        """Parses dense coordinates into structural CSR arrays."""
        current_non_zero_count = 0
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                val = dense_matrix[r][c]
                if val != 0.0:
                    self.values.append(val)
                    self.col_indices.append(c)
                    current_non_zero_count += 1
            self.row_pointers.append(current_non_zero_count)

    def get_element(self, row: int, col: int) -> float:
        """Retrieves an individual element value at a specific coordinate via binary index lookup."""
        if not (0 <= row < self.num_rows) or not (0 <= col < self.num_cols):
            raise IndexError("Requested matrix coordinates map outside valid boundaries.")
            
        start_idx = self.row_pointers[row]
        end_idx = self.row_pointers[row + 1]
        
        # Linear search through the column segment of the requested row
        for i in range(start_idx, end_idx):
            if self.col_indices[i] == col:
                return self.values[i]
                
        return 0.0


if __name__ == "__main__":
    sparse_data = [
        [1.5, 0.0, 0.0, 0.0],
        [0.0, 0.0, 3.2, 0.0],
        [0.0, 0.0, 0.0, 4.1]
    ]
    
    csr = CompressedSparseRowMatrix(sparse_data)
    print(f"Compressed Non-Zero Values: {csr.values}")
    print(f"Row Range Pointers: {csr.row_pointers}")
    print(f"Element Lookup at (1, 2): {csr.get_element(1, 2)}")