# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Long Short-Term Memory (LSTM) Cell Gating
Description: Constructs the Forget, Input, and Output gates required to protect
             the internal Cell State, effectively resolving vanishing gradients.
"""
import numpy as np  # type: ignore
from typing import Tuple


class LSTMCellEngine:
    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-x))

    @staticmethod
    def lstm_step(x_t: np.ndarray, h_prev: np.ndarray, C_prev: np.ndarray,
                  W: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        
        # Concatenate hidden state and input vector
        concat_in = np.vstack((h_prev, x_t))
        
        # Single matrix multiply for all 4 gates (optimized computation)
        Z = np.dot(W, concat_in) + b
        
        # Split output into exactly 4 equal-sized gate matrices
        H = h_prev.shape[0]
        f_gate = LSTMCellEngine.sigmoid(Z[0:H, :])        # Forget gate
        i_gate = LSTMCellEngine.sigmoid(Z[H:2*H, :])      # Input gate
        C_candidate = np.tanh(Z[2*H:3*H, :])              # Candidate cell state
        o_gate = LSTMCellEngine.sigmoid(Z[3*H:4*H, :])    # Output gate
        
        # Element-wise cell state update (The "Constant Error Carousel")
        C_t = (f_gate * C_prev) + (i_gate * C_candidate)
        
        # Hidden state output
        h_t = o_gate * np.tanh(C_t)
        
        return h_t, C_t


if __name__ == "__main__":
    np.random.seed(42)
    # H = 4, input = 3. Concat dim = 7
    H_dim = 4
    In_dim = 3
    
    W_fused = np.random.randn(4 * H_dim, H_dim + In_dim)  # (16, 7)
    b_fused = np.zeros((4 * H_dim, 1))                    # (16, 1)
    
    h0 = np.zeros((H_dim, 1))
    C0 = np.zeros((H_dim, 1))
    x1 = np.random.randn(In_dim, 1)
    
    h1, C1 = LSTMCellEngine.lstm_step(x1, h0, C0, W_fused, b_fused)
    
    assert h1.shape == (H_dim, 1)
    assert C1.shape == (H_dim, 1)
    
    print(f"[TASK 03 PASSED] LSTM step calculated. Fused matrices cleanly split and executed.")