# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Gini Impurity Evaluator
Description: Computes Gini Impurity, the primary operational metric utilized by 
             Decision Trees (like CART) to minimize misclassification probabilities.
"""
import numpy as np  # type: ignore


class GiniImpurityEngine:
    @staticmethod
    def compute_gini(labels: np.ndarray) -> float:
        if len(labels) == 0:
            return 0.0
            
        _, counts = np.unique(labels, return_counts=True)
        probabilities = counts / len(labels)
        
        # Gini Formula: 1 - sum(p_i^2)
        gini = 1.0 - np.sum(np.square(probabilities))
        return float(gini)


if __name__ == "__main__":
    # Perfect homogenous node (Gini = 0.0)
    homogenous_node = np.array(["cat", "cat", "cat", "cat"])
    
    # Perfectly split binary node (Gini = 0.5)
    split_node = np.array(["cat", "dog", "cat", "dog"])
    
    gini_homo = GiniImpurityEngine.compute_gini(homogenous_node)
    gini_split = GiniImpurityEngine.compute_gini(split_node)
    
    assert gini_homo == 0.0
    assert abs(gini_split - 0.5) < 1e-6
    
    print(f"[TASK 02 PASSED] Gini Impurity validated. Homogenous Node: {gini_homo:.2f} | Split Node: {gini_split:.2f}")