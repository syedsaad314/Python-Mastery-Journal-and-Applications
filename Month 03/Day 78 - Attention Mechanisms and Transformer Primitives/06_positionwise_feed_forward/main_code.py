# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Position-Wise Feed-Forward Networks (FFN)
Description: Projects contextualized attention outputs into expanded higher-dimensional 
             latents, applying non-linearities independently across identical token positions.
"""
import numpy as np  # type: ignore


class PositionwiseFeedForwardEngine:
    def __init__(self, d_model: int, d_ff: int):
        np.random.seed(42)
        # W1: Expansion layer
        self.W1 = np.random.randn(d_model, d_ff) * 0.01
        self.b1 = np.zeros((d_ff,))
        
        # W2: Compression layer
        self.W2 = np.random.randn(d_ff, d_model) * 0.01
        self.b2 = np.zeros((d_model,))

    def forward(self, x: np.ndarray) -> np.ndarray:
        # x shape: (batch_size, seq_len, d_model)
        
        # 1. Expand dimension: Linear + ReLU
        # np.dot automatically handles batched matrix mult on the last dimension of x
        hidden = np.maximum(0, np.dot(x, self.W1) + self.b1)
        
        # 2. Compress back to d_model: Linear
        output = np.dot(hidden, self.W2) + self.b2
        
        return output


if __name__ == "__main__":
    d_model = 512
    d_ff = 2048  # Transformer standard: expand internal projection by 4x
    
    ffn = PositionwiseFeedForwardEngine(d_model, d_ff)
    
    # Batch=2, Seq=10, Embed=512
    batch_input = np.random.randn(2, 10, 512)
    
    ffn_out = ffn.forward(batch_input)
    
    # Output must perfectly map back to input geometry
    assert ffn_out.shape == (2, 10, 512)
    
    print(f"[TASK 06 PASSED] Position-wise Feed-Forward expanded to d_ff={d_ff} and re-compressed to d_model={d_model}.")