# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Multi-Head Attention Dimensional Splitting
Description: Fragments high-dimensional Q/K/V tensors into multiple parallel heads
             to capture distinct semantic relationships simultaneously.
"""
import numpy as np  # type: ignore


class MultiHeadAttentionEngine:
    @staticmethod
    def split_heads(x: np.ndarray, num_heads: int) -> np.ndarray:
        # x shape: (batch_size, seq_len, embed_dim)
        batch_size, seq_len, embed_dim = x.shape
        
        if embed_dim % num_heads != 0:
            raise ValueError(f"Embedding dimension {embed_dim} must be divisible by num_heads {num_heads}.")
            
        head_dim = embed_dim // num_heads
        
        # 1. Reshape to (batch_size, seq_len, num_heads, head_dim)
        reshaped = x.reshape(batch_size, seq_len, num_heads, head_dim)
        
        # 2. Transpose to group by heads: (batch_size, num_heads, seq_len, head_dim)
        # This aligns the memory so batch matmuls operate cleanly per-head
        split_tensor = reshaped.transpose(0, 2, 1, 3)
        return split_tensor

    @staticmethod
    def concatenate_heads(x: np.ndarray) -> np.ndarray:
        # Revert: (batch_size, num_heads, seq_len, head_dim) -> (batch_size, seq_len, embed_dim)
        batch_size, num_heads, seq_len, head_dim = x.shape
        
        # Transpose back to (batch_size, seq_len, num_heads, head_dim)
        transposed = x.transpose(0, 2, 1, 3)
        
        # Flatten the last two dimensions to recover the original embed_dim
        concat_tensor = transposed.reshape(batch_size, seq_len, num_heads * head_dim)
        return concat_tensor


if __name__ == "__main__":
    # Batch=2, Seq_len=5, Embed_dim=16
    input_tensor = np.arange(160, dtype=np.float64).reshape(2, 5, 16)
    
    # Split into 4 heads. Expected Head_dim = 16 / 4 = 4
    heads_tensor = MultiHeadAttentionEngine.split_heads(input_tensor, num_heads=4)
    
    assert heads_tensor.shape == (2, 4, 5, 4)
    
    # Reassemble and ensure lossless mathematical reconstruction
    reconstructed_tensor = MultiHeadAttentionEngine.concatenate_heads(heads_tensor)
    
    assert reconstructed_tensor.shape == (2, 5, 16)
    assert np.array_equal(input_tensor, reconstructed_tensor)
    
    print(f"[TASK 02 PASSED] Multi-Head splitting/concatenation verified. Split Shape: {heads_tensor.shape}")