# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Convolutional Backward Propagation
Description: Derives gradients for filter weights and previous inputs using 
             180-degree filter rotation and full cross-correlation mechanics.
"""
import numpy as np  # type: ignore


class ConvBackwardEngine:
    @staticmethod
    def backward_pass(dZ: np.ndarray, A_prev: np.ndarray, W_kernel: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        # A_prev: (i_h, i_w), W_kernel: (f_h, f_w), dZ: (out_h, out_w)
        i_h, i_w = A_prev.shape
        f_h, f_w = W_kernel.shape
        
        # 1. Gradient with respect to Weights (dW)
        # dW is the valid cross-correlation of A_prev and dZ
        dW = np.zeros_like(W_kernel)
        for h in range(f_h):
            for w in range(f_w):
                A_slice = A_prev[h:h+dZ.shape[0], w:w+dZ.shape[1]]
                dW[h, w] = np.sum(A_slice * dZ)
                
        # 2. Gradient with respect to previous activations (dA_prev)
        # dA_prev is the FULL convolution of dZ with the 180-degree rotated filter
        dA_prev = np.zeros_like(A_prev)
        # Pad dZ so full convolution works out exactly to A_prev shape
        pad_h, pad_w = f_h - 1, f_w - 1
        dZ_padded = np.pad(dZ, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
        W_rotated = np.rot90(W_kernel, 2)
        
        for h in range(i_h):
            for w in range(i_w):
                dZ_slice = dZ_padded[h:h+f_h, w:w+f_w]
                dA_prev[h, w] = np.sum(dZ_slice * W_rotated)
                
        return dA_prev, dW


if __name__ == "__main__":
    A_in = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float64)
    W_f = np.array([[1, 0], [0, -1]], dtype=np.float64)
    dZ_out = np.array([[2, 1], [0, -1]], dtype=np.float64) # Gradient upstream
    
    dA, dW_filter = ConvBackwardEngine.backward_pass(dZ_out, A_in, W_f)
    
    assert dA.shape == A_in.shape
    assert dW_filter.shape == W_f.shape
    assert np.all(np.isfinite(dA))
    
    print(f"[TASK 05 PASSED] Convolutional Backprop executed. Gradient dW mapped correctly:\n{dW_filter}")