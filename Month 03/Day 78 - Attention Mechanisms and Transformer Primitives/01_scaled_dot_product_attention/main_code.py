# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Scaled Dot-Product Attention
Description: Implements the mathematical heart of the Transformer, calculating
             contextual weights via Query, Key, and Value matrix multiplications.
"""
import numpy as np  # type: ignore


class AttentionEngine:
    @staticmethod
    def compute_scaled_attention(Q: np.ndarray, K: np.ndarray, V: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        # Dimensions: Q (seq_len_q, d_k), K (seq_len_k, d_k), V (seq_len_v, d_v)
        # Note: seq_len_k must equal seq_len_v.
        d_k = Q.shape[-1]
        
        # 1. Compute unscaled raw attention scores: Q * K^T
        # Shape: (seq_len_q, seq_len_k)
        scores = np.dot(Q, K.T)
        
        # 2. Scale by square root of d_k to stabilize Softmax gradients
        scaled_scores = scores / np.sqrt(d_k)
        
        # 3. Softmax along the Key sequence dimension (axis=-1)
        # Numerically stable softmax
        shifted_scores = scaled_scores - np.max(scaled_scores, axis=-1, keepdims=True)
        exp_scores = np.exp(shifted_scores)
        attention_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
        
        # 4. Contextualize the Values: Weights * V
        # Shape: (seq_len_q, d_v)
        context_vector = np.dot(attention_weights, V)
        
        return context_vector, attention_weights


if __name__ == "__main__":
    np.random.seed(42)
    # Sequence length of 3, embedding dimension of 4
    queries = np.random.randn(3, 4)
    keys = np.random.randn(3, 4)
    values = np.random.randn(3, 4)
    
    context, attn_weights = AttentionEngine.compute_scaled_attention(queries, keys, values)
    
    # Assert contextual output maps back to Q's sequence length and V's dimension
    assert context.shape == (3, 4)
    assert attn_weights.shape == (3, 3)
    
    # Assert softmax probabilities sum to 1.0 across the Key dimension
    assert np.allclose(np.sum(attn_weights, axis=-1), 1.0)
    
    print(f"[TASK 01 PASSED] Scaled Dot-Product Attention computed. Context Matrix Shape: {context.shape}")