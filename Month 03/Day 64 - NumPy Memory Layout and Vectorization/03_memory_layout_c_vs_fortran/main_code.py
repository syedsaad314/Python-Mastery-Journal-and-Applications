# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Contiguous Memory Layouts (C-Major vs Fortran-Major)
Description: Analyzes CPU cache alignment impacts between Row-Major (C-contiguous) 
             and Column-Major (Fortran-contiguous) multi-dimensional arrays.
"""
import numpy as np # type: ignore

class MemoryLayoutAnalyzer:
    @staticmethod
    def generate_layout_pair(rows: int, cols: int) -> tuple[np.ndarray, np.ndarray]:
        c_array = np.zeros((rows, cols), dtype=np.float64, order='C')
        f_array = np.zeros((rows, cols), dtype=np.float64, order='F')
        return c_array, f_array

if __name__ == "__main__":
    c_grid, f_grid = MemoryLayoutAnalyzer.generate_layout_pair(100, 50)
    
    # Verify internal flags for layout correctness
    assert c_grid.flags['C_CONTIGUOUS'] is True
    assert c_grid.flags['F_CONTIGUOUS'] is False
    
    assert f_grid.flags['C_CONTIGUOUS'] is False
    assert f_grid.flags['F_CONTIGUOUS'] is True
    
    # Transposing a C-contiguous array produces a Fortran-contiguous view without copying memory
    c_transposed = c_grid.T
    assert c_transposed.flags['F_CONTIGUOUS'] is True
    assert c_transposed.base is c_grid
    
    print("[TASK 03 PASSED] C-Contiguous and Fortran-Contiguous memory flags and transposition views verified.")