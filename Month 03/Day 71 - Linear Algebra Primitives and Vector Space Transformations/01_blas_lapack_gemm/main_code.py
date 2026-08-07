# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: High-Performance Matrix Multiplication (BLAS GEMM)
Description: Utilizes numpy's internal C-bindings to BLAS (Basic Linear Algebra Subprograms)
             for highly optimized General Matrix Multiplication (GEMM).
"""
import numpy as np  # type: ignore


class MatrixMultiplicationEngine:
    @staticmethod
    def compute_gemm(mat_a: np.ndarray, mat_b: np.ndarray) -> np.ndarray:
        # np.dot routes directly to the highly optimized BLAS dgemm/sgemm routines
        # bypassing Python-level loops entirely.
        return np.dot(mat_a, mat_b)


if __name__ == "__main__":
    # 2x3 Matrix
    A = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0]
    ], dtype=np.float64)
    
    # 3x2 Matrix
    B = np.array([
        [7.0, 8.0],
        [9.0, 1.0],
        [2.0, 3.0]
    ], dtype=np.float64)
    
    result = MatrixMultiplicationEngine.compute_gemm(A, B)
    
    # Result should be 2x2
    assert result.shape == (2, 2)
    # (1*7 + 2*9 + 3*2) = 7 + 18 + 6 = 31
    assert result[0, 0] == 31.0
    
    print(f"[TASK 01 PASSED] BLAS GEMM Matrix multiplication completed successfully:\n{result}")