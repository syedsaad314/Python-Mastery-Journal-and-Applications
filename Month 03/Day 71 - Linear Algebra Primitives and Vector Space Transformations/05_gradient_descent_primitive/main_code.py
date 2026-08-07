# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Vectorized Gradient Descent Primitive
Description: Implements a raw vectorized gradient descent step for a linear model,
             updating weights by computing gradients using matrix calculus.
"""
import numpy as np  # type: ignore


class GradientDescentEngine:
    @staticmethod
    def compute_step(X: np.ndarray, y: np.ndarray, weights: np.ndarray, learning_rate: float) -> np.ndarray:
        m = len(y)
        
        # 1. Forward pass: compute predictions
        predictions = np.dot(X, weights)
        
        # 2. Compute error
        error = predictions - y
        
        # 3. Compute gradient: (1/m) * X^T * Error
        gradient = (1 / m) * np.dot(X.T, error)
        
        # 4. Update weights
        new_weights = weights - (learning_rate * gradient)
        
        return new_weights


if __name__ == "__main__":
    # 3 samples, 2 features (including bias term)
    X_train = np.array([
        [1.0, 2.0],
        [1.0, 3.0],
        [1.0, 4.0]
    ], dtype=np.float64)
    
    # Target values
    y_train = np.array([5.0, 7.0, 9.0], dtype=np.float64)
    
    # Initial weights [bias, w1]
    w_init = np.array([0.0, 0.0], dtype=np.float64)
    
    w_updated = GradientDescentEngine.compute_step(X_train, y_train, w_init, learning_rate=0.1)
    
    assert w_updated.shape == (2,)
    # Gradients dictate weights should increase (positive correlation)
    assert w_updated[1] > 0.0 
    
    print(f"[TASK 05 PASSED] Vectorized gradient step computed. New Weights: {w_updated}")