# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Vectorized Confusion Matrix Primitive
Description: Computes multi-class classification evaluation metrics (True Positives,
             False Negatives, etc.) without iterative nested looping.
"""
import numpy as np  # type: ignore


class ConfusionMatrixEngine:
    @staticmethod
    def compute_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int) -> np.ndarray:
        # Validate data shapes
        if y_true.shape != y_pred.shape:
            raise ValueError("True labels and predictions must be identically shaped arrays.")
            
        # Transform 2D coordinates (true, pred) into a 1D flat index array
        # Formula: true_label * num_classes + pred_label
        linear_indices = y_true * num_classes + y_pred
        
        # Bincount tallies the occurrences of each unique linear index instantly in C
        flat_confusion = np.bincount(linear_indices, minlength=num_classes**2)
        
        # Reshape the flat counts back into the N x N confusion matrix
        return flat_confusion.reshape((num_classes, num_classes))


if __name__ == "__main__":
    # Classes: 0, 1, 2
    true_labels = np.array([2, 0, 2, 2, 0, 1])
    predictions = np.array([0, 0, 2, 2, 0, 2])
    
    conf_matrix = ConfusionMatrixEngine.compute_confusion_matrix(true_labels, predictions, num_classes=3)
    
    assert conf_matrix.shape == (3, 3)
    # 2 true '0's predicted correctly as '0'
    assert conf_matrix[0, 0] == 2
    # 1 true '1' misclassified as '2'
    assert conf_matrix[1, 2] == 1
    # 2 true '2's predicted correctly as '2'
    assert conf_matrix[2, 2] == 2
    
    print(f"[TASK 05 PASSED] Vectorized Confusion Matrix resolved successfully:\n{conf_matrix}")