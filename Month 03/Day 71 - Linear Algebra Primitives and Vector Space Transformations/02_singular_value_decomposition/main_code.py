# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Singular Value Decomposition (SVD)
Description: Factors a real matrix into orthogonal and diagonal matrices, acting
             as the mathematical engine for PCA and dimensionality reduction.
"""
import numpy as np  # type: ignore


class SVDEngine:
    @staticmethod
    def decompose_and_reconstruct(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        # Compute SVD: A = U * S * V^T
        U, S_vals, Vt = np.linalg.svd(matrix, full_matrices=False)
        
        # Convert singular values vector into a diagonal matrix
        S_matrix = np.diag(S_vals)
        
        # Reconstruct original matrix to verify decomposition losslessness
        reconstructed = np.dot(U, np.dot(S_matrix, Vt))
        
        return U, S_vals, Vt, reconstructed


if __name__ == "__main__":
    X = np.array([
        [1.0, 2.0],
        [3.0, 4.0],
        [5.0, 6.0]
    ], dtype=np.float64)
    
    U, S, Vt, X_reconstructed = SVDEngine.decompose_and_reconstruct(X)
    
    assert U.shape == (3, 2)
    assert S.shape == (2,)
    assert Vt.shape == (2, 2)
    assert np.allclose(X, X_reconstructed, atol=1e-8)
    
    print(f"[TASK 02 PASSED] SVD computed. Singular values extracted: {S}")