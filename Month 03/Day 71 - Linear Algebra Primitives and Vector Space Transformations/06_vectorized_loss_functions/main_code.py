# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Vectorized Loss Functions (MSE & Log Loss)
Description: Calculates Machine Learning error metrics across full dataset arrays
             in a single SIMD-optimized pass.
"""
import numpy as np  # type: ignore


class LossFunctionEngine:
    @staticmethod
    def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        # MSE = (1/n) * sum((y_true - y_pred)^2)
        return np.mean(np.square(y_true - y_pred))

    @staticmethod
    def binary_cross_entropy(y_true: np.ndarray, y_pred_prob: np.ndarray) -> float:
        # Clip probabilities to prevent log(0) - Infinity errors
        epsilon = 1e-15
        y_pred_clipped = np.clip(y_pred_prob, epsilon, 1 - epsilon)
        
        # Log Loss = -(1/n) * sum(y * log(p) + (1-y) * log(1-p))
        loss = -np.mean(y_true * np.log(y_pred_clipped) + (1 - y_true) * np.log(1 - y_pred_clipped))
        return loss


if __name__ == "__main__":
    y_actual = np.array([1.0, 0.0, 1.0], dtype=np.float64)
    y_predicted_prob = np.array([0.9, 0.1, 0.8], dtype=np.float64)
    
    mse = LossFunctionEngine.mean_squared_error(y_actual, y_predicted_prob)
    bce = LossFunctionEngine.binary_cross_entropy(y_actual, y_predicted_prob)
    
    assert mse > 0.0
    assert bce > 0.0
    # Closer predictions yield lower loss
    assert mse < 0.1 
    
    print(f"[TASK 06 PASSED] Loss Metrics calculated. MSE: {mse:.4f} | BCE: {bce:.4f}")