# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: ReLU & Leaky ReLU Non-Linearities (Forward & Backward)
Description: Implements the Rectified Linear Unit and its Leaky variant alongside 
             their exact analytical derivatives for backpropagation.
"""
import numpy as np  # type: ignore
from typing import Tuple


class ReLUEngine:
    @staticmethod
    def relu_forward(Z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        # f(z) = max(0, z)
        A = np.maximum(0, Z)
        cache = Z  # Cached for backward pass
        return A, cache

    @staticmethod
    def relu_backward(dA: np.ndarray, cache: np.ndarray) -> np.ndarray:
        Z = cache
        dZ = np.array(dA, copy=True)
        # Derivative is 0 where Z <= 0, and 1 where Z > 0
        dZ[Z <= 0] = 0
        return dZ

    @staticmethod
    def leaky_relu_forward(Z: np.ndarray, alpha: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
        # f(z) = z if z > 0 else alpha * z
        A = np.where(Z > 0, Z, Z * alpha)
        cache = Z
        return A, cache

    @staticmethod
    def leaky_relu_backward(dA: np.ndarray, cache: np.ndarray, alpha: float = 0.01) -> np.ndarray:
        Z = cache
        dZ = np.array(dA, copy=True)
        # Derivative is alpha where Z <= 0, and 1 where Z > 0
        dZ[Z <= 0] *= alpha
        return dZ


if __name__ == "__main__":
    test_Z = np.array([[-1.0, 2.0], [-3.0, 4.0]], dtype=np.float64)
    upstream_dA = np.ones_like(test_Z)  # Incoming gradient matrix
    
    # ReLU Tests
    A_relu, cache_r = ReLUEngine.relu_forward(test_Z)
    dZ_relu = ReLUEngine.relu_backward(upstream_dA, cache_r)
    
    assert A_relu[0, 0] == 0.0 and A_relu[0, 1] == 2.0
    assert dZ_relu[0, 0] == 0.0 and dZ_relu[0, 1] == 1.0
    
    # Leaky ReLU Tests
    A_leaky, cache_l = ReLUEngine.leaky_relu_forward(test_Z, alpha=0.1)
    dZ_leaky = ReLUEngine.leaky_relu_backward(upstream_dA, cache_l, alpha=0.1)
    
    assert A_leaky[0, 0] == -0.1
    assert dZ_leaky[0, 0] == 0.1
    
    print(f"[TASK 01 PASSED] ReLU and Leaky ReLU forward/backward primitives verified mathematically.")