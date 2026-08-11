# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Sigmoid & Tanh Squashing Activations (Forward & Backward)
Description: Implements logistic curve mathematical activations mapping continuous 
             inputs into tight probabilistic boundaries [0, 1] or [-1, 1].
"""
import numpy as np  # type: ignore
from typing import Tuple


class SquashingActivationEngine:
    @staticmethod
    def sigmoid_forward(Z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        # f(z) = 1 / (1 + e^-z)
        A = 1.0 / (1.0 + np.exp(-Z))
        cache = A  # Cache activation A for efficient derivative computation
        return A, cache

    @staticmethod
    def sigmoid_backward(dA: np.ndarray, cache: np.ndarray) -> np.ndarray:
        A = cache
        # Derivative of Sigmoid: A * (1 - A)
        dZ = dA * A * (1.0 - A)
        return dZ

    @staticmethod
    def tanh_forward(Z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        # f(z) = (e^z - e^-z) / (e^z + e^-z) -> NumPy handles this natively
        A = np.tanh(Z)
        cache = A
        return A, cache

    @staticmethod
    def tanh_backward(dA: np.ndarray, cache: np.ndarray) -> np.ndarray:
        A = cache
        # Derivative of Tanh: 1 - A^2
        dZ = dA * (1.0 - np.square(A))
        return dZ


if __name__ == "__main__":
    Z_input = np.array([0.0, 100.0, -100.0], dtype=np.float64)
    dA_input = np.ones_like(Z_input)
    
    # Sigmoid
    A_sig, cache_sig = SquashingActivationEngine.sigmoid_forward(Z_input)
    dZ_sig = SquashingActivationEngine.sigmoid_backward(dA_input, cache_sig)
    
    assert A_sig[0] == 0.5  # Sigmoid of 0 is 0.5
    assert abs(A_sig[1] - 1.0) < 1e-6  # Saturates at 1
    assert abs(dZ_sig[1] - 0.0) < 1e-6 # Derivative vanishes at extremes
    
    # Tanh
    A_tanh, cache_tanh = SquashingActivationEngine.tanh_forward(Z_input)
    dZ_tanh = SquashingActivationEngine.tanh_backward(dA_input, cache_tanh)
    
    assert A_tanh[0] == 0.0  # Tanh of 0 is 0
    assert abs(A_tanh[2] + 1.0) < 1e-6  # Saturates at -1
    
    print(f"[TASK 02 PASSED] Sigmoid and Tanh logistic curves bounded and derived successfully.")