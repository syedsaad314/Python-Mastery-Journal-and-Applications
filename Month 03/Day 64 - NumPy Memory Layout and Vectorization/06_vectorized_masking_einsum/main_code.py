# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Tensor Contraction Efficiency via Einstein Summation
Description: Leverages np.einsum for high-speed multi-dimensional matrix operations,
             bypassing intermediate transpositions and unrolled explicit loops.
"""
import numpy as np # type: ignore

class TensorContractionEngine:
    @staticmethod
    def compute_matrix_vector_dot(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
        # Standard matrix-vector product: result[i] = sum_j (matrix[i,j] * vector[j])
        return np.einsum('ij,j->i', matrix, vector)

    @staticmethod
    def compute_batch_trace(batch_matrices: np.ndarray) -> np.ndarray:
        # Computes trace across a batch of 2D matrices: result[b] = sum_i (matrices[b,i,i])
        return np.einsum('bii->b', batch_matrices)

if __name__ == "__main__":
    A = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)
    x = np.array([0.5, 2.0], dtype=np.float64)
    
    # Matrix-Vector Multiplication Validation
    y = TensorContractionEngine.compute_matrix_vector_dot(A, x)
    assert np.array_equal(y, [4.5, 9.5])
    
    # Batch Trace Computation Validation (Batch size = 2)
    batch_mats = np.array([
        [[1, 2], [3, 4]],   # Trace = 1 + 4 = 5
        [[10, 0], [0, 20]]  # Trace = 10 + 20 = 30
    ], dtype=np.int64)
    traces = TensorContractionEngine.compute_batch_trace(batch_mats)
    assert np.array_equal(traces, [5, 30])
    
    print(f"[TASK 06 PASSED] Einstein summation matrix contraction and batch traces verified: {traces}")