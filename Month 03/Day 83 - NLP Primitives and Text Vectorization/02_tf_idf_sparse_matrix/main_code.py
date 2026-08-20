# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: TF-IDF Vectorization Matrix
Description: Maps a corpus of documents into term-frequency inverse-document-frequency 
             vectors, penalizing ubiquitous stop-words automatically using logarithms.
"""
import numpy as np  # type: ignore
from typing import Tuple


class TFIDFEngine:
    @staticmethod
    def compute_tf_idf(corpus: list[list[str]], vocab: list[str]) -> Tuple[np.ndarray, np.ndarray]:
        num_docs = len(corpus)
        num_terms = len(vocab)
        
        # Initialize Term Frequency (TF) matrix
        tf_matrix = np.zeros((num_docs, num_terms), dtype=np.float64)
        
        for i, doc in enumerate(corpus):
            for j, term in enumerate(vocab):
                tf_matrix[i, j] = doc.count(term)
                
        # Document Frequency (DF): Number of documents containing the term
        df_vector = np.sum(tf_matrix > 0, axis=0)
        
        # Inverse Document Frequency (IDF): log( (1 + N) / (1 + DF) ) + 1
        # Smooths division by zero and ensures terms that appear in all docs aren't strictly 0
        idf_vector = np.log((1.0 + num_docs) / (1.0 + df_vector)) + 1.0
        
        # TF-IDF calculation
        tfidf_matrix = tf_matrix * idf_vector
        
        # L2 Normalize the matrix along the document axis
        norms = np.linalg.norm(tfidf_matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0  # Prevent division by zero
        tfidf_matrix_normalized = tfidf_matrix / norms
        
        return tfidf_matrix_normalized, idf_vector


if __name__ == "__main__":
    docs = [
        ["the", "cat", "sat", "on", "the", "mat"],
        ["the", "dog", "barked"],
        ["the", "cat", "meowed"]
    ]
    vocabulary = ["the", "cat", "dog", "mat"]
    
    tfidf_mat, idf_vec = TFIDFEngine.compute_tf_idf(docs, vocabulary)
    
    assert tfidf_mat.shape == (3, 4)
    assert idf_vec.shape == (4,)
    
    # 'the' appears in all 3 documents, so its IDF should be the lowest
    idx_the = vocabulary.index("the")
    idx_mat = vocabulary.index("mat")
    assert idf_vec[idx_the] < idf_vec[idx_mat]
    
    # Assert L2 normalization worked (row sum of squares == 1.0)
    assert np.allclose(np.sum(np.square(tfidf_mat), axis=1), 1.0)
    
    print(f"[TASK 02 PASSED] Normalized TF-IDF matrix computed. Shape: {tfidf_mat.shape}")