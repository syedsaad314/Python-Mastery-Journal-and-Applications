# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Linear Backward Propagation (Chain Rule Calculus)
Description: Calculates local gradients (dW, db, dA_prev) with respect to the cost function
             using the cached affine forward inputs and upstream gradients (dZ).
"""
import numpy as np  # type: ignore
from typing import Tuple


class ChainRuleEngine:
    @staticmethod
    def linear_backward(dZ: np.ndarray, cache: tuple) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        A_prev, W, b = cache
        m_batch_size = A_prev.shape[1]
        
        # dW = (1/m) * dZ * A_prev^T
        dW = (1.0 / m_batch_size) * np.dot(dZ, A_prev.T)
        
        # db = (1/m) * sum(dZ, axis=1) -> Keep dims ensures (n_out, 1) broadcast shape remains intact
        db = (1.0 / m_batch_size) * np.sum(dZ, axis=1, keepdims=True)
        
        # dA_prev = W^T * dZ (Calculated to pass backwards to the next preceding layer)
        dA_prev = np.dot(W.T, dZ)
        
        return dA_prev, dW, db


if __name__ == "__main__":
    np.random.seed(99)
    # Define shapes: 2 neurons out, 3 features in, batch size 4
    dZ_upstream = np.random.randn(2, 4)
    A_prev_cache = np.random.randn(3, 4)
    W_cache = np.random.randn(2, 3)
    b_cache = np.random.randn(2, 1)
    
    linear_cache = (A_prev_cache, W_cache, b_cache)
    
    dA_prev, dW, db = ChainRuleEngine.linear_backward(dZ_upstream, linear_cache)
    
    # Assert structural bounds matching exactly with forward parameter shapes
    assert dA_prev.shape == A_prev_cache.shape  # (3, 4)
    assert dW.shape == W_cache.shape            # (2, 3)
    assert db.shape == b_cache.shape            # (2, 1)
    
    print(f"[TASK 04 PASSED] Matrix Calculus Chain Rule applied. Local gradients isolated correctly.")