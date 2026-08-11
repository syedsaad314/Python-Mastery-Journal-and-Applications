# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Early Stopping Heuristics
Description: Monitors validation loss trajectories during training loops to 
             automatically halt execution when model generalization diverges.
"""
import numpy as np  # type: ignore
from typing import Optional


class EarlyStoppingEngine:
    def __init__(self, patience: int = 5, min_delta: float = 0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = float('inf')
        self.wait_count = 0
        self.best_weights: Optional[np.ndarray] = None
        self.stop_training = False

    def check_criteria(self, current_loss: float, current_weights: np.ndarray) -> bool:
        if current_loss < (self.best_loss - self.min_delta):
            # Significant improvement detected
            self.best_loss = current_loss
            self.best_weights = np.copy(current_weights)
            self.wait_count = 0
        else:
            # Model is stagnating or degrading
            self.wait_count += 1
            if self.wait_count >= self.patience:
                self.stop_training = True
                
        return self.stop_training


if __name__ == "__main__":
    stopper = EarlyStoppingEngine(patience=2, min_delta=0.01)
    dummy_weights = np.array([1.0])
    
    # Epoch 1: Loss = 1.0 (Improvement)
    assert stopper.check_criteria(1.0, dummy_weights) is False
    # Epoch 2: Loss = 0.995 (No significant improvement, wait = 1)
    assert stopper.check_criteria(0.995, dummy_weights) is False
    # Epoch 3: Loss = 0.999 (No improvement, wait = 2 -> STOPS)
    assert stopper.check_criteria(0.999, dummy_weights) is True
    
    print(f"[TASK 04 PASSED] Early stopping triggered cleanly after {stopper.patience} epochs of stagnation.")