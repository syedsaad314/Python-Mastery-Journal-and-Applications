# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Vectorized Euclidean & Cosine Distances
Description: Computes geometric distances between high-dimensional vectors 
             using pure NumPy linear algebra primitives.
"""
import numpy as np  # type: ignore


class DistanceMetricEngine:
    @staticmethod
    def euclidean_distance(v1: np.ndarray, v2: np.ndarray) -> float:
        # L2 Norm of the difference vector
        return np.linalg.norm(v1 - v2)

    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        # Dot product divided by the product of L2 norms
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
            
        return dot_product / (norm_v1 * norm_v2)


if __name__ == "__main__":
    vec_a = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    vec_b = np.array([0.0, 1.0, 0.0], dtype=np.float64)
    vec_c = np.array([2.0, 0.0, 0.0], dtype=np.float64)
    
    euclidean_val = DistanceMetricEngine.euclidean_distance(vec_a, vec_b)
    # sqrt(1^2 + 1^2) = sqrt(2) ~ 1.414
    assert abs(euclidean_val - np.sqrt(2)) < 1e-6
    
    # Orthogonal vectors -> cosine similarity = 0.0
    cosine_ab = DistanceMetricEngine.cosine_similarity(vec_a, vec_b)
    assert abs(cosine_ab - 0.0) < 1e-6
    
    # Parallel vectors -> cosine similarity = 1.0
    cosine_ac = DistanceMetricEngine.cosine_similarity(vec_a, vec_c)
    assert abs(cosine_ac - 1.0) < 1e-6
    
    print(f"[TASK 03 PASSED] Vectorized Euclidean and Cosine distances computed successfully.")