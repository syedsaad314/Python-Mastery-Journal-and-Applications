# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Numerically Stable Softmax with Temperature Scaling
Description: Transforms unnormalized logits into stable probability distributions,
             using temperature scaling to control prediction confidence entropy.
"""
import numpy as np  # type: ignore


class SoftmaxPrimitiveEngine:
    @staticmethod
    def compute_stable_softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        if temperature <= 0:
            raise ValueError("Temperature must be greater than zero.")
            
        # Shift logits by the maximum value to prevent np.exp() numeric overflow
        shifted_logits = logits - np.max(logits, axis=-1, keepdims=True)
        
        # Apply temperature scaling
        scaled_logits = shifted_logits / temperature
        
        # Softmax computation
        exponents = np.exp(scaled_logits)
        probabilities = exponents / np.sum(exponents, axis=-1, keepdims=True)
        
        return probabilities


if __name__ == "__main__":
    raw_logits = np.array([2.0, 1.0, 0.1], dtype=np.float64)
    
    # Standard softmax
    probs_standard = SoftmaxPrimitiveEngine.compute_stable_softmax(raw_logits, temperature=1.0)
    
    # High temperature (Smoothing the probabilities closer to uniform)
    probs_high_t = SoftmaxPrimitiveEngine.compute_stable_softmax(raw_logits, temperature=5.0)
    
    # Assert proper probability distribution criteria
    assert abs(np.sum(probs_standard) - 1.0) < 1e-6
    assert abs(np.sum(probs_high_t) - 1.0) < 1e-6
    
    # High temperature should have a lower maximum confidence than standard
    assert np.max(probs_high_t) < np.max(probs_standard)
    
    print(f"[TASK 04 PASSED] Softmax executed cleanly. Standard Peak: {np.max(probs_standard):.2%} | Hot Peak: {np.max(probs_high_t):.2%}")