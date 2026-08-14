# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Sinusoidal Positional Encoding
Description: Injects sequence order metadata into embedding vectors using mathematically
             continuous interleaving sine and cosine frequency waves.
"""
import numpy as np  # type: ignore


class PositionalEncodingEngine:
    @staticmethod
    def generate_positional_encodings(seq_len: int, embed_dim: int) -> np.ndarray:
        if embed_dim % 2 != 0:
            raise ValueError("Embedding dimension must be an even number.")
            
        # 1. Initialize matrices for positions (0 to seq_len-1) and dimensions (0 to embed_dim-1)
        positions = np.arange(seq_len)[:, np.newaxis]        # Shape: (seq_len, 1)
        dimensions = np.arange(0, embed_dim, 2)[np.newaxis, :] # Shape: (1, embed_dim/2)
        
        # 2. Compute the scaling factor: 1 / (10000 ^ (2i / d_model))
        div_term = np.exp(dimensions * -(np.log(10000.0) / embed_dim))
        
        # 3. Create the encoding matrix
        pe_matrix = np.zeros((seq_len, embed_dim), dtype=np.float64)
        
        # 4. Apply Sine to even indices (0, 2, 4...)
        pe_matrix[:, 0::2] = np.sin(positions * div_term)
        
        # 5. Apply Cosine to odd indices (1, 3, 5...)
        pe_matrix[:, 1::2] = np.cos(positions * div_term)
        
        return pe_matrix


if __name__ == "__main__":
    seq_length = 50
    dimension = 128
    
    pos_enc = PositionalEncodingEngine.generate_positional_encodings(seq_length, dimension)
    
    assert pos_enc.shape == (50, 128)
    
    # Assert sine applied to index 0, cosine to index 1
    # sin(0) = 0.0, cos(0) = 1.0 for position 0
    assert pos_enc[0, 0] == 0.0
    assert pos_enc[0, 1] == 1.0
    
    # Assert frequency decay across depth
    assert pos_enc[1, 0] != pos_enc[1, 126]  # Highly variable frequencies
    
    print(f"[TASK 04 PASSED] Sinusoidal Positional Encodings mapped. Shape: {pos_enc.shape}")