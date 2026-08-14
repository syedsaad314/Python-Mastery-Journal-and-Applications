# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Causal (Look-Ahead) Attention Masking
Description: Generates an upper-triangular negative infinity mask to prevent 
             autoregressive models from "cheating" by looking into the future.
"""
import numpy as np  # type: ignore


class CausalMaskEngine:
    @staticmethod
    def create_causal_mask(seq_len: int) -> np.ndarray:
        # Create a matrix of 1s, then zero out the upper triangle (excluding diagonal)
        # Using np.tril (lower triangle of an array)
        mask = np.tril(np.ones((seq_len, seq_len), dtype=np.float64))
        
        # Convert 0s (future tokens) to -Infinity, and 1s (past/current tokens) to 0
        causal_mask = np.where(mask == 0, -1e9, 0.0)
        return causal_mask

    @staticmethod
    def apply_mask_to_scores(raw_scores: np.ndarray, mask: np.ndarray) -> np.ndarray:
        # raw_scores shape: (seq_len, seq_len)
        # Mask broadcast addition
        return raw_scores + mask


if __name__ == "__main__":
    seq_length = 4
    mask = CausalMaskEngine.create_causal_mask(seq_length)
    
    assert mask.shape == (4, 4)
    # The first token can only see itself (row 0: 0, -1e9, -1e9, -1e9)
    assert mask[0, 1] == -1e9
    assert mask[0, 0] == 0.0
    # The last token can see everything (row 3: 0, 0, 0, 0)
    assert np.all(mask[3] == 0.0)
    
    # Simulate application
    dummy_scores = np.ones((4, 4), dtype=np.float64)
    masked_scores = CausalMaskEngine.apply_mask_to_scores(dummy_scores, mask)
    
    assert masked_scores[0, 1] == -1e9 + 1.0  # Mathematically neg-inf representation
    
    print(f"[TASK 03 PASSED] Causal Mask generated and applied:\n{mask}")