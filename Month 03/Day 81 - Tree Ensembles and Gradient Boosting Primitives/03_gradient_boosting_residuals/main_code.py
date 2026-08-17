# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Gradient Boosting Residual Matcher
Description: Computes pseudo-residuals (negative gradients) to train sequential models,
             enabling additive models to correct the errors of preceding stages.
"""
import numpy as np  # type: ignore


class GradientBoostingEngine:
    @staticmethod
    def calculate_pseudo_residuals(y_true: np.ndarray, current_predictions: np.ndarray, loss_type: str = 'mse') -> np.ndarray:
        if loss_type == 'mse':
            # Loss = 0.5 * (y - pred)^2
            # Negative Gradient w.r.t prediction = y - pred
            residuals = y_true - current_predictions
        elif loss_type == 'log_loss':
            # Negative Gradient for Binary Logistic Regression
            # First map predictions through sigmoid
            probs = 1.0 / (1.0 + np.exp(-current_predictions))
            residuals = y_true - probs
        else:
            raise ValueError("Unsupported loss metric.")
            
        return residuals


if __name__ == "__main__":
    y_ground_truth = np.array([10.0, 20.0, 30.0], dtype=np.float64)
    
    # Stage 0: Initial prediction is simply the mean of all targets
    initial_pred = np.full_like(y_ground_truth, fill_value=np.mean(y_ground_truth))
    
    # Stage 1: Calculate residuals
    residuals = GradientBoostingEngine.calculate_pseudo_residuals(y_ground_truth, initial_pred, loss_type='mse')
    
    # Mean of targets is 20.0
    # Residuals: [10 - 20, 20 - 20, 30 - 20] = [-10.0, 0.0, 10.0]
    assert np.array_equal(initial_pred, [20.0, 20.0, 20.0])
    assert np.array_equal(residuals, [-10.0, 0.0, 10.0])
    
    print(f"[TASK 03 PASSED] Gradient Boosting Pseudo-Residuals calculated:\nTarget: {y_ground_truth}\nResiduals: {residuals}")