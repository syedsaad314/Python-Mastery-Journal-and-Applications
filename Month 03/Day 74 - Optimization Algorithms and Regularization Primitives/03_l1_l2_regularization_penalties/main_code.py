# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: L1 (Lasso) and L2 (Ridge) Regularization
Description: Computes forward penalty terms and backward gradient adjustments 
             to prevent weight explosion and enforce sparsity.
"""
import numpy as np  # type: ignore


class RegularizationEngine:
    @staticmethod
    def l2_ridge_penalty(weights: np.ndarray, lambda_reg: float) -> tuple[float, np.ndarray]:
        # Penalty (Loss term): 0.5 * lambda * sum(w^2)
        penalty = 0.5 * lambda_reg * np.sum(np.square(weights))
        
        # Gradient adjustment: lambda * w
        gradient_penalty = lambda_reg * weights
        return penalty, gradient_penalty

    @staticmethod
    def l1_lasso_penalty(weights: np.ndarray, lambda_reg: float) -> tuple[float, np.ndarray]:
        # Penalty (Loss term): lambda * sum(|w|)
        penalty = lambda_reg * np.sum(np.abs(weights))
        
        # Gradient adjustment: lambda * sign(w)
        gradient_penalty = lambda_reg * np.sign(weights)
        return penalty, gradient_penalty


if __name__ == "__main__":
    w = np.array([2.0, -3.0, 0.0], dtype=np.float64)
    lam = 0.1
    
    l2_loss, l2_grad = RegularizationEngine.l2_ridge_penalty(w, lam)
    l1_loss, l1_grad = RegularizationEngine.l1_lasso_penalty(w, lam)
    
    # L2 = 0.5 * 0.1 * (4 + 9 + 0) = 0.65
    assert abs(l2_loss - 0.65) < 1e-6
    # L1 = 0.1 * (2 + 3 + 0) = 0.5
    assert abs(l1_loss - 0.5) < 1e-6
    
    assert np.array_equal(l1_grad, np.array([0.1, -0.1, 0.0]))
    
    print(f"[TASK 03 PASSED] L1 and L2 Regularization penalties and gradients calculated securely.")