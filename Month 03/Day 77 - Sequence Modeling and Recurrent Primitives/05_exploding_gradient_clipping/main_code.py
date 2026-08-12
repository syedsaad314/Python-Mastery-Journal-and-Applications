# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: L2 Norm Gradient Clipping
Description: Enforces a maximum magnitude cap on gradient vectors to prevent numerical
             overflows (Exploding Gradients) common in unrolled BPTT.
"""
import numpy as np  # type: ignore


class GradientClippingEngine:
    @staticmethod
    def clip_by_l2_norm(gradients: dict, max_norm: float = 1.0) -> dict:
        # 1. Compute global L2 norm across all gradient matrices combined
        sum_sq = 0.0
        for grad in gradients.values():
            sum_sq += np.sum(np.square(grad))
            
        global_norm = np.sqrt(sum_sq)
        
        # 2. Check if clipping is necessary
        if global_norm > max_norm:
            scale_factor = max_norm / global_norm
            # Scale down all gradients uniformly preserving vector direction
            for key in gradients.keys():
                gradients[key] *= scale_factor
                
        return gradients


if __name__ == "__main__":
    # Simulate an exploding gradient matrix during BPTT
    exploding_grads = {
        "dW_xh": np.array([[100.0, -250.0], [50.0, 300.0]]),
        "dW_hh": np.array([[1000.0, 0.0], [0.0, -1200.0]])
    }
    
    # Calculate original magnitude manually
    orig_sum = np.sum(np.square(exploding_grads["dW_xh"])) + np.sum(np.square(exploding_grads["dW_hh"]))
    orig_norm = np.sqrt(orig_sum)
    assert orig_norm > 1500.0  # Massive explosion
    
    # Apply clipping cap at 5.0
    clipped_grads = GradientClippingEngine.clip_by_l2_norm(exploding_grads, max_norm=5.0)
    
    # Verify new global magnitude is exactly bounded
    new_sum = np.sum(np.square(clipped_grads["dW_xh"])) + np.sum(np.square(clipped_grads["dW_hh"]))
    new_norm = np.sqrt(new_sum)
    
    assert abs(new_norm - 5.0) < 1e-6
    
    print(f"[TASK 05 PASSED] Gradient explosion suppressed. Norm reduced from {orig_norm:.2f} to {new_norm:.2f}")