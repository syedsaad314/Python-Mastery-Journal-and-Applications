# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Naive Recurrent Neural Network (RNN) Forward Pass
Description: Processes sequential data by recursively updating an internal 
             hidden state memory vector across discrete time steps.
"""
import numpy as np  # type: ignore
from typing import List, Tuple


class NaiveRNNEngine:
    @staticmethod
    def rnn_forward(X_seq: List[np.ndarray], h_prev: np.ndarray, 
                    W_xh: np.ndarray, W_hh: np.ndarray, b_h: np.ndarray) -> Tuple[List[np.ndarray], np.ndarray]:
        
        hidden_states = []
        h_current = h_prev
        
        # Iterate over unrolled time steps
        for x_t in X_seq:
            # h_t = tanh(W_hh * h_{t-1} + W_xh * x_t + b_h)
            h_current = np.tanh(np.dot(W_hh, h_current) + np.dot(W_xh, x_t) + b_h)
            hidden_states.append(h_current)
            
        return hidden_states, h_current


if __name__ == "__main__":
    np.random.seed(42)
    # Dimensions: Input=3, Hidden=4
    W_xh_init = np.random.randn(4, 3)
    W_hh_init = np.random.randn(4, 4)
    b_h_init = np.zeros((4, 1), dtype=np.float64)
    
    # 3 Time Steps of Data (each of shape 3, 1)
    sequence = [np.random.randn(3, 1) for _ in range(3)]
    
    # Initial Zero State
    h0 = np.zeros((4, 1), dtype=np.float64)
    
    all_states, final_state = NaiveRNNEngine.rnn_forward(sequence, h0, W_xh_init, W_hh_init, b_h_init)
    
    assert len(all_states) == 3
    assert final_state.shape == (4, 1)
    
    # Assert values are bounded by Tanh squashing (-1 to 1)
    assert np.all((final_state >= -1.0) & (final_state <= 1.0))
    
    print(f"[TASK 01 PASSED] Naive RNN processed sequence of length 3. Final Hidden State:\n{final_state.flatten()}")