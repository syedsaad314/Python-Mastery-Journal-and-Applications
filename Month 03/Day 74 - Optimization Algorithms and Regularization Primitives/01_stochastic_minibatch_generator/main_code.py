# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Stochastic Mini-Batch Generator
Description: Efficiently slices datasets into randomized mini-batches for 
             stochastic gradient descent without duplicating the dataset in memory.
"""
import numpy as np  # type: ignore
from typing import Generator, Tuple


class MiniBatchEngine:
    @staticmethod
    def generate_batches(X: np.ndarray, y: np.ndarray, batch_size: int, shuffle: bool = True) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        if len(X) != len(y):
            raise ValueError("Features and labels must have the same number of samples.")
            
        m_samples = len(X)
        indices = np.arange(m_samples)
        
        if shuffle:
            rng = np.random.default_rng(42)
            rng.shuffle(indices)
            
        for start_idx in range(0, m_samples, batch_size):
            end_idx = min(start_idx + batch_size, m_samples)
            batch_indices = indices[start_idx:end_idx]
            
            # Yield memory slices (views) where possible to avoid copy overhead
            yield X[batch_indices], y[batch_indices]


if __name__ == "__main__":
    X_data = np.arange(10).reshape(10, 1)  # 10 samples
    y_data = np.arange(10)
    
    batches = list(MiniBatchEngine.generate_batches(X_data, y_data, batch_size=3, shuffle=False))
    
    # 10 samples / 3 batch size = 4 batches (3, 3, 3, 1)
    assert len(batches) == 4
    assert len(batches[0][0]) == 3
    assert len(batches[-1][0]) == 1  # Remainder batch
    
    print(f"[TASK 01 PASSED] Mini-batch generator executed. Total batches generated: {len(batches)}")