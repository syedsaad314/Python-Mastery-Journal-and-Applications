# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Eigenvalue Decomposition (Eigendecomposition)
Description: Extracts eigenvalues and eigenvectors from a square covariance matrix
             to identify the directions of maximum data spread.
"""
import numpy as np  # type: ignore


class EigendecompositionEngine:
    @staticmethod
    def extract_principal_components(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        # 1. Mean-center the data
        centered_data = data - np.mean(data, axis=0)
        
        # 2. Compute the covariance matrix
        # rowvar=False treats columns as variables (features)
        cov_matrix = np.cov(centered_data, rowvar=False)
        
        # 3. Perform eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        
        # 4. Sort eigenvalues and eigenvectors in descending order
        sorted_indices = np.argsort(eigenvalues)[::-1]
        sorted_eigenvalues = eigenvalues[sorted_indices]
        sorted_eigenvectors = eigenvectors[:, sorted_indices]
        
        return sorted_eigenvalues, sorted_eigenvectors


if __name__ == "__main__":
    # Synthetic dataset: 5 samples, 3 features
    dataset = np.array([
        [2.5, 2.4, 0.5],
        [0.5, 0.7, 0.1],
        [2.2, 2.9, 1.5],
        [1.9, 2.2, 0.2],
        [3.1, 3.0, 1.1]
    ], dtype=np.float64)
    
    evals, evecs = EigendecompositionEngine.extract_principal_components(dataset)
    
    assert evals.shape == (3,)
    assert evecs.shape == (3, 3)
    # Assert sorted descending
    assert evals[0] >= evals[1] >= evals[2]
    
    print(f"[TASK 04 PASSED] Eigendecomposition complete. Top eigenvalue: {evals[0]:.4f}")