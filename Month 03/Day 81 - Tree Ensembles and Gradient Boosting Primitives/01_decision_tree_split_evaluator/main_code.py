# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Information Gain Split Evaluator
Description: Evaluates potential numerical split points for a Decision Tree node,
             calculating the exact Information Gain (Gini drop) mathematically.
"""
import numpy as np  # type: ignore


class SplitEvaluatorEngine:
    @staticmethod
    def gini_impurity(labels: np.ndarray) -> float:
        if len(labels) == 0:
            return 0.0
        _, counts = np.unique(labels, return_counts=True)
        probs = counts / len(labels)
        return float(1.0 - np.sum(np.square(probs)))

    @staticmethod
    def evaluate_split(features: np.ndarray, labels: np.ndarray, split_value: float) -> tuple[float, np.ndarray, np.ndarray]:
        # Generate boolean mask for splitting
        left_mask = features <= split_value
        right_mask = ~left_mask
        
        left_labels = labels[left_mask]
        right_labels = labels[right_mask]
        
        # Calculate parent impurity
        parent_gini = SplitEvaluatorEngine.gini_impurity(labels)
        
        # Calculate weighted child impurities
        n = len(labels)
        n_l, n_r = len(left_labels), len(right_labels)
        
        if n_l == 0 or n_r == 0:
            return 0.0, left_mask, right_mask  # Zero information gain if split is empty
            
        gini_left = SplitEvaluatorEngine.gini_impurity(left_labels)
        gini_right = SplitEvaluatorEngine.gini_impurity(right_labels)
        
        # Information Gain: Parent - Weighted Average of Children
        info_gain = parent_gini - ((n_l / n) * gini_left + (n_r / n) * gini_right)
        
        return info_gain, left_mask, right_mask


if __name__ == "__main__":
    # 6 samples, 1 feature
    X_feat = np.array([1.0, 2.0, 3.0, 8.0, 9.0, 10.0])
    y_target = np.array([0, 0, 0, 1, 1, 1])  # Perfectly separable at X = 5.0
    
    # Test an optimal split
    ig_optimal, l_mask, r_mask = SplitEvaluatorEngine.evaluate_split(X_feat, y_target, split_value=5.0)
    
    # Test a terrible split (all data goes to one side or splits pure classes)
    ig_bad, _, _ = SplitEvaluatorEngine.evaluate_split(X_feat, y_target, split_value=1.5)
    
    # Gini of [0,0,0,1,1,1] is 0.5. Splitting at 5.0 yields [0,0,0] (Gini 0) and [1,1,1] (Gini 0)
    # Gain should be exactly 0.5 - 0.0 = 0.5
    assert abs(ig_optimal - 0.5) < 1e-6
    assert ig_optimal > ig_bad
    assert np.sum(l_mask) == 3
    
    print(f"[TASK 01 PASSED] Information Gain calculated. Optimal Split Gain: {ig_optimal:.4f} | Bad Split Gain: {ig_bad:.4f}")