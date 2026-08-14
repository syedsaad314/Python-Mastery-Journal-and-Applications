# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Layer Normalization Primitive
Description: Standardizes numerical distributions dynamically across the embedding 
             feature dimension of each individual token independently of batch size.
"""
import numpy as np  # type: ignore


class LayerNormalizationEngine:
    @staticmethod
    def layer_norm_forward(x: np.ndarray, gamma: np.ndarray, beta: np.ndarray, epsilon: float = 1e-5) -> np.ndarray:
        # x shape: (batch_size, seq_len, embed_dim)
        
        # 1. Compute mean and variance strictly across the LAST dimension (embed_dim)
        # keepdims=True ensures shapes remain (batch, seq, 1) for broadcasting
        mean = np.mean(x, axis=-1, keepdims=True)
        variance = np.var(x, axis=-1, keepdims=True)
        
        # 2. Normalize
        x_norm = (x - mean) / np.sqrt(variance + epsilon)
        
        # 3. Scale and Shift using learnable parameters (gamma, beta)
        out = gamma * x_norm + beta
        return out


if __name__ == "__main__":
    np.random.seed(42)
    # Batch=2, Seq=3, Embed=4
    inputs = np.random.randn(2, 3, 4) * 5.0 + 10.0  # Unnormalized data
    
    g_scale = np.ones(4, dtype=np.float64)
    b_shift = np.zeros(4, dtype=np.float64)
    
    normalized_output = LayerNormalizationEngine.layer_norm_forward(inputs, g_scale, b_shift)
    
    # Assert dimensions are strictly maintained
    assert normalized_output.shape == (2, 3, 4)
    
    # Verify the normalization logic: The mean of the features for any single token should be 0
    token_mean = np.mean(normalized_output[0, 0, :])
    token_var = np.var(normalized_output[0, 0, :])
    
    assert np.allclose(token_mean, 0.0, atol=1e-6)
    assert np.allclose(token_var, 1.0, atol=1e-6)
    
    print(f"[TASK 05 PASSED] Layer Normalization stabilized feature magnitudes per-token cleanly.")