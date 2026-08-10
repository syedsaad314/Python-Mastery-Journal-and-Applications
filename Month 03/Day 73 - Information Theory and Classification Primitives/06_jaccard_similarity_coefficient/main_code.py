# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Jaccard Similarity (Intersection over Union)
Description: Computes similarity matrices for binary classification, set analysis, 
             and sparse document overlaps utilizing bitwise boolean algebra.
"""
import numpy as np  # type: ignore


class JaccardSimilarityEngine:
    @staticmethod
    def compute_iou(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        if not np.array_equal(np.unique(y_true), [0, 1]) and len(np.unique(y_true)) > 2:
             # Soft-fail logic check if arrays contain continuous floating point data
             raise ValueError("Jaccard arrays must be boolean or binary integer formats.")
             
        # Compute bitwise Intersection (Logical AND)
        intersection = np.logical_and(y_true, y_pred)
        
        # Compute bitwise Union (Logical OR)
        union = np.logical_or(y_true, y_pred)
        
        union_sum = np.sum(union)
        if union_sum == 0:
            return 1.0  # Perfect overlap (both sets completely empty)
            
        return float(np.sum(intersection) / union_sum)


if __name__ == "__main__":
    mask_true = np.array([1, 1, 0, 1, 0, 0, 1], dtype=np.int8)
    mask_pred = np.array([1, 0, 0, 1, 0, 1, 1], dtype=np.int8)
    
    jaccard_score = JaccardSimilarityEngine.compute_iou(mask_true, mask_pred)
    
    # Intersection: [1, 0, 0, 1, 0, 0, 1] -> Sum = 3
    # Union:        [1, 1, 0, 1, 0, 1, 1] -> Sum = 5
    # Expected IOU: 3/5 = 0.6
    assert abs(jaccard_score - 0.6) < 1e-6
    
    print(f"[TASK 06 PASSED] Binary Jaccard Coefficient (IoU) evaluated accurately: {jaccard_score:.2f}")