# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Gated Recurrent Unit (GRU) Matrix Primitive
Description: Evaluates a leaner alternative to the LSTM that merges the cell 
             and hidden state using Update and Reset gates.
"""
import numpy as np  # type: ignore
from typing import Tuple


class GRUCellEngine:
    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-x))

    @staticmethod
    def gru_step(x_t: np.ndarray, h_prev: np.ndarray, 
                 W_z: np.ndarray, W_r: np.ndarray, W_h: np.ndarray) -> np.ndarray:
        
        concat_in = np.vstack((h_prev, x_t))
        
        # 1. Update Gate (Controls how much past information to keep)
        z_t = GRUCellEngine.sigmoid(np.dot(W_z, concat_in))
        
        # 2. Reset Gate (Controls how much past information to forget)
        r_t = GRUCellEngine.sigmoid(np.dot(W_r, concat_in))
        
        # 3. Candidate Hidden State (Applies reset gate to history)
        concat_reset = np.vstack((r_t * h_prev, x_t))
        h_candidate = np.tanh(np.dot(W_h, concat_reset))
        
        # 4. Final Hidden State (Linear interpolation via Update gate)
        h_t = (1.0 - z_t) * h_prev + z_t * h_candidate
        
        return h_t


if __name__ == "__main__":
    np.random.seed(99)
    H_dim, In_dim = 4, 3
    concat_len = H_dim + In_dim
    
    Wz = np.random.randn(H_dim, concat_len)
    Wr = np.random.randn(H_dim, concat_len)
    Wh = np.random.randn(H_dim, concat_len)
    
    h_init = np.zeros((H_dim, 1))
    x_input = np.random.randn(In_dim, 1)
    
    h_next = GRUCellEngine.gru_step(x_input, h_init, Wz, Wr, Wh)
    
    assert h_next.shape == (H_dim, 1)
    assert np.all((h_next >= -1.0) & (h_next <= 1.0))
    
    print(f"[TASK 04 PASSED] GRU step calculated successfully. Hidden state updated via Reset/Update gates.")