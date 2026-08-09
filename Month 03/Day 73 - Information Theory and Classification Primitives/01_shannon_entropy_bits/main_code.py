# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Shannon Entropy (Information Theory)
Description: Calculates the theoretical information entropy (in bits) of a dataset,
             measuring the inherent unpredictability or impurity of the class labels.
"""
import numpy as np  # type: ignore


class EntropyEngine:
    @staticmethod
    def calculate_shannon_entropy(labels: np.ndarray) -> float:
        if len(labels) == 0:
            return 0.0
            
        # Count frequencies of unique labels
        _, counts = np.unique(labels, return_counts=True)
        
        # Calculate probabilities
        probabilities = counts / len(labels)
        
        # Shannon Entropy Formula: H(X) = -sum(p_i * log2(p_i))
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return float(entropy)


if __name__ == "__main__":
    # Highly predictable dataset (Low Entropy)
    pure_data = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0])
    
    # Completely random/unpredictable dataset (Maximum Entropy for binary is 1.0)
    mixed_data = np.array([1, 0, 1, 0, 1, 0, 1, 0])
    
    entropy_pure = EntropyEngine.calculate_shannon_entropy(pure_data)
    entropy_mixed = EntropyEngine.calculate_shannon_entropy(mixed_data)
    
    assert entropy_pure < 0.5
    assert abs(entropy_mixed - 1.0) < 1e-6
    
    print(f"[TASK 01 PASSED] Shannon Entropy calculated. Pure: {entropy_pure:.4f} bits | Mixed: {entropy_mixed:.4f} bits")