# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Adam Optimizer (Adaptive Moment Estimation)
Description: Computes parameter updates using exponentially decaying averages of 
             past gradients (momentum) and squared gradients (RMSProp).
"""
import numpy as np  # type: ignore


class AdamOptimizerEngine:
    def __init__(self, learning_rate: float = 0.001, beta1: float = 0.9, beta2: float = 0.999, epsilon: float = 1e-8):
        self.lr = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None  # First moment (Mean)
        self.v = None  # Second moment (Uncentered Variance)
        self.t = 0     # Timestep

    def compute_update(self, weights: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        if self.m is None or self.v is None:
            self.m = np.zeros_like(weights)
            self.v = np.zeros_like(weights)
            
        self.t += 1
        
        # Update biased first moment estimate
        self.m = self.beta1 * self.m + (1 - self.beta1) * gradients
        # Update biased second raw moment estimate
        self.v = self.beta2 * self.v + (1 - self.beta2) * np.square(gradients)
        
        # Compute bias-corrected first moment estimate
        m_hat = self.m / (1 - self.beta1 ** self.t)
        # Compute bias-corrected second raw moment estimate
        v_hat = self.v / (1 - self.beta2 ** self.t)
        
        # Apply update rule
        updated_weights = weights - (self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon))
        return updated_weights


if __name__ == "__main__":
    adam = AdamOptimizerEngine(learning_rate=0.1)
    
    w_initial = np.array([0.5, -0.2], dtype=np.float64)
    grads = np.array([0.1, -0.05], dtype=np.float64)
    
    # Run one step
    w_updated = adam.compute_update(w_initial, grads)
    
    assert w_updated.shape == (2,)
    assert adam.t == 1
    # Weight 0 should decrease (gradient is positive), Weight 1 should increase (gradient is negative)
    assert w_updated[0] < 0.5
    assert w_updated[1] > -0.2
    
    print(f"[TASK 02 PASSED] Adam optimizer vector step executed. Updated weights: {w_updated}")