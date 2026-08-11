# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Inverted Dropout Regularization Matrix
Description: Stochastically drops neurons during training to prevent co-adaptation,
             using the inverted scale method to keep inference unscaled.
"""
import numpy as np  # type: ignore
from typing import Tuple


class InvertedDropoutEngine:
    @staticmethod
    def dropout_forward(A: np.ndarray, keep_prob: float) -> Tuple[np.ndarray, np.ndarray]:
        if not (0.0 < keep_prob <= 1.0):
            raise ValueError("Keep probability must be bounded within (0, 1].")
            
        # 1. Generate boolean mask matrix via Uniform Distribution
        # np.random.rand generates [0, 1), so rand < keep_prob generates True for keeping
        rng = np.random.default_rng()
        D_mask = (rng.random(A.shape) < keep_prob).astype(np.float64)
        
        # 2. Shut down specific neurons
        A_dropped = A * D_mask
        
        # 3. Inverted Scaling: Divide by keep_prob to retain mathematical expected values
        A_dropped /= keep_prob
        
        return A_dropped, D_mask

    @staticmethod
    def dropout_backward(dA: np.ndarray, D_mask: np.ndarray, keep_prob: float) -> np.ndarray:
        # Shut down gradients for neurons that were turned off during forward pass
        dA_dropped = dA * D_mask
        # Re-apply the identical inverted scale factor
        dA_dropped /= keep_prob
        return dA_dropped


if __name__ == "__main__":
    A_input = np.ones((5, 10000), dtype=np.float64)  # 5 neurons, 10k batch size
    keep_p = 0.8
    
    A_out, mask = InvertedDropoutEngine.dropout_forward(A_input, keep_prob=keep_p)
    dA_out = InvertedDropoutEngine.dropout_backward(np.ones_like(A_out), mask, keep_prob=keep_p)
    
    # Statistical validation (Law of Large Numbers)
    retained_ratio = np.sum(mask) / mask.size
    assert abs(retained_ratio - keep_p) < 0.05
    
    # Scaled values for kept neurons should be exactly (1.0 / 0.8) = 1.25
    assert np.max(A_out) == 1.25
    assert np.min(A_out) == 0.0
    
    print(f"[TASK 05 PASSED] Inverted Dropout scaled correctly. Retained Ratio: {retained_ratio:.2%}")