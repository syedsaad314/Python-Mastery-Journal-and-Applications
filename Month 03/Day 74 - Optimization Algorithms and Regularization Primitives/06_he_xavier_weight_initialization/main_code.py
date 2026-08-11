# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Variance-Preserving Weight Initializations
Description: Implements He (Kaiming) and Xavier (Glorot) initializers to prevent 
             vanishing and exploding gradients in deep neural networks.
"""
import numpy as np  # type: ignore


class WeightInitializationEngine:
    @staticmethod
    def xavier_initialization(fan_in: int, fan_out: int) -> np.ndarray:
        # Ideal for Sigmoid/Tanh activations
        # Draw from normal dist with variance = 2 / (fan_in + fan_out)
        limit = np.sqrt(2.0 / (fan_in + fan_out))
        rng = np.random.default_rng(42)
        return rng.normal(0, limit, size=(fan_in, fan_out))

    @staticmethod
    def he_initialization(fan_in: int, fan_out: int) -> np.ndarray:
        # Ideal for ReLU variants
        # Draw from normal dist with variance = 2 / fan_in
        limit = np.sqrt(2.0 / fan_in)
        rng = np.random.default_rng(99)
        return rng.normal(0, limit, size=(fan_in, fan_out))


if __name__ == "__main__":
    n_in, n_out = 1000, 500
    
    w_xavier = WeightInitializationEngine.xavier_initialization(n_in, n_out)
    w_he = WeightInitializationEngine.he_initialization(n_in, n_out)
    
    assert w_xavier.shape == (1000, 500)
    assert w_he.shape == (1000, 500)
    
    # He initialization variance should roughly equal 2 / fan_in (2/1000 = 0.002)
    he_variance = np.var(w_he)
    assert abs(he_variance - 0.002) < 1e-3
    
    print(f"[TASK 06 PASSED] Weight matrices initialized natively. He Variance matches distribution target: {he_variance:.4f}")