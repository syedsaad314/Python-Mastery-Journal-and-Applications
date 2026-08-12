# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Backpropagation Through Time (BPTT)
Description: Accumulates gradients across unrolled recurrent time steps to update 
             shared sequence weights, demonstrating the source of vanishing gradients.
"""
import numpy as np  # type: ignore


class BPTTEngine:
    @staticmethod
    def rnn_backward(dh_final: np.ndarray, hidden_states: list, X_seq: list, 
                     W_hh: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        
        dW_xh = np.zeros((W_hh.shape[0], X_seq[0].shape[0]))
        dW_hh = np.zeros_like(W_hh)
        db_h = np.zeros((W_hh.shape[0], 1))
        
        # Gradient passed from the future into the current step
        dh_next = dh_final
        
        # Unroll backward through time
        for t in reversed(range(len(X_seq))):
            h_t = hidden_states[t]
            h_prev = hidden_states[t-1] if t > 0 else np.zeros_like(h_t)
            x_t = X_seq[t]
            
            # Derivative of tanh: (1 - h_t^2)
            dtanh = (1.0 - np.square(h_t)) * dh_next
            
            # Accumulate gradients across shared parameters
            dW_xh += np.dot(dtanh, x_t.T)
            dW_hh += np.dot(dtanh, h_prev.T)
            db_h += dtanh
            
            # Pass gradient back to the previous time step
            dh_next = np.dot(W_hh.T, dtanh)
            
        return dW_xh, dW_hh, db_h


if __name__ == "__main__":
    np.random.seed(99)
    # Mocking shapes: hidden=4, input=3
    h_states_mock = [np.random.randn(4, 1) for _ in range(3)]
    X_mock = [np.random.randn(3, 1) for _ in range(3)]
    Whh_mock = np.random.randn(4, 4)
    dh_upstream = np.random.randn(4, 1)
    
    dWxh, dWhh, dbh = BPTTEngine.rnn_backward(dh_upstream, h_states_mock, X_mock, Whh_mock)
    
    assert dWxh.shape == (4, 3)
    assert dWhh.shape == (4, 4)
    assert dbh.shape == (4, 1)
    
    print(f"[TASK 02 PASSED] BPTT executed across 3 unrolled time steps. Gradients accumulated successfully.")