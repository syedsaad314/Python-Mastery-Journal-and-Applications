# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Second-Order Newton-Raphson Step (XGBoost Math)
Description: Evaluates optimal leaf weights utilizing both the Gradient (First-Order) 
             and Hessian (Second-Order) Taylor expansions with L2 regularization.
"""
import numpy as np  # type: ignore


class XGBoostMathEngine:
    @staticmethod
    def calculate_optimal_leaf_weight(gradients: np.ndarray, hessians: np.ndarray, reg_lambda: float = 1.0) -> float:
        # XGBoost Optimal Leaf Weight Equation: w* = -sum(g_i) / (sum(h_i) + lambda)
        sum_grad = np.sum(gradients)
        sum_hess = np.sum(hessians)
        
        # Prevent division by zero mathematically
        if sum_hess + reg_lambda == 0:
            return 0.0
            
        optimal_weight = - (sum_grad / (sum_hess + reg_lambda))
        return float(optimal_weight)

    @staticmethod
    def calculate_similarity_score(gradients: np.ndarray, hessians: np.ndarray, reg_lambda: float = 1.0) -> float:
        # Score used to evaluate split quality: sum(g_i)^2 / (sum(h_i) + lambda)
        sum_grad = np.sum(gradients)
        sum_hess = np.sum(hessians)
        
        similarity = (sum_grad ** 2) / (sum_hess + reg_lambda)
        return float(similarity)


if __name__ == "__main__":
    # Assume 3 samples fall into this specific tree leaf node
    g_arr = np.array([-0.5, -0.2, 0.1])  # Gradients
    h_arr = np.array([0.25, 0.25, 0.25]) # Hessians (e.g., from Logistic Loss)
    
    # Calculate optimal weight update for this leaf
    weight = XGBoostMathEngine.calculate_optimal_leaf_weight(g_arr, h_arr, reg_lambda=1.0)
    score = XGBoostMathEngine.calculate_similarity_score(g_arr, h_arr, reg_lambda=1.0)
    
    # sum_g = -0.6. sum_h = 0.75. lambda = 1.0. 
    # w* = -(-0.6) / (0.75 + 1.0) = 0.6 / 1.75 ≈ 0.3428
    assert abs(weight - 0.342857) < 1e-5
    assert score > 0.0
    
    print(f"[TASK 04 PASSED] XGBoost Second-Order Newton Step processed. Optimal Leaf Weight: {weight:.4f}")