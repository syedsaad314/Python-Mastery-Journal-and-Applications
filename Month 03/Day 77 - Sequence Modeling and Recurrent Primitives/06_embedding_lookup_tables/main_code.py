# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Dense Embedding Lookup Tables
Description: Implements an O(1) integer array-indexing primitive to bypass 
             O(N) sparse one-hot matrix multiplications in sequence architectures.
"""
import numpy as np  # type: ignore


class EmbeddingTableEngine:
    def __init__(self, vocab_size: int, embed_dim: int):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        # Initialize dense embedding matrix randomly
        np.random.seed(42)
        self.E_matrix = np.random.randn(vocab_size, embed_dim)

    def forward_lookup(self, word_indices: list[int]) -> np.ndarray:
        # Validate vocab bounds
        if any(idx < 0 or idx >= self.vocab_size for idx in word_indices):
            raise IndexError("Word index out of vocabulary bounds.")
            
        # O(1) Native C-array slicing indexing
        # Replaces np.dot(one_hot_vector, E_matrix)
        dense_vectors = self.E_matrix[word_indices]
        return dense_vectors


if __name__ == "__main__":
    # Vocabulary of 10,000 words, mapping to 256-dimensional dense vectors
    embed_engine = EmbeddingTableEngine(vocab_size=10000, embed_dim=256)
    
    # Retrieve embeddings for token indices [50, 9999, 0]
    token_sequence = [50, 9999, 0]
    sequence_embeddings = embed_engine.forward_lookup(token_sequence)
    
    assert sequence_embeddings.shape == (3, 256)
    
    # Verify the values exactly match the specific row in the lookup table
    assert np.array_equal(sequence_embeddings[0], embed_engine.E_matrix[50])
    
    print(f"[TASK 06 PASSED] O(1) Embedding Lookup extracted shape: {sequence_embeddings.shape}")