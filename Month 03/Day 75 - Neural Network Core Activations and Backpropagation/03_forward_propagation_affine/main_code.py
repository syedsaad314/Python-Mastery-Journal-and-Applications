# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Affine Transformation (Forward Linear Layer)
Description: Computes the foundational linear hypothesis mapping Z = WX + b 
             using high-speed BLAS matrix multiplication.
"""
import numpy as np  # type: ignore
from typing import Tuple


class AffineTransformEngine:
    @staticmethod
    def linear_forward(A_prev: np.ndarray, W: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, tuple]:
        # Z = W * A_prev + b
        # A_prev shape: (features_in, batch_size)
        # W shape: (neurons_out, features_in)
        # b shape: (neurons_out, 1) -> Broadcasted across batch_size
        
        Z = np.dot(W, A_prev) + b
        
        # Cache dimensions and inputs required strictly for backpropagation calculations
        cache = (A_prev, W, b)
        return Z, cache


if __name__ == "__main__":
    np.random.seed(42)
    # 3 features input, batch size of 4
    A_in = np.random.randn(3, 4)
    # 2 output neurons in this layer, connecting to 3 input features
    W_layer = np.random.randn(2, 3)
    # Bias vector (2 neurons)
    b_layer = np.random.randn(2, 1)
    
    Z_out, cached_data = AffineTransformEngine.linear_forward(A_in, W_layer, b_layer)
    
    # Output Z must be (neurons_out, batch_size) -> (2, 4)
    assert Z_out.shape == (2, 4)
    assert len(cached_data) == 3
    
    print(f"[TASK 03 PASSED] Forward Affine Transform executed. Z Shape: {Z_out.shape} | Matrix Math OK.")