# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Okapi BM25 Ranking Algorithm
Description: Enhances TF-IDF for search engines by implementing term-frequency 
             saturation and document-length normalization to prevent long-doc bias.
"""
import numpy as np  # type: ignore


class BM25Engine:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b

    def compute_scores(self, query_terms: list[str], corpus: list[list[str]]) -> np.ndarray:
        num_docs = len(corpus)
        doc_lengths = np.array([len(doc) for doc in corpus], dtype=np.float64)
        avg_doc_len = np.mean(doc_lengths)
        
        scores = np.zeros(num_docs, dtype=np.float64)
        
        for term in query_terms:
            # Calculate Document Frequency (DF) for the term
            df = sum(1 for doc in corpus if term in doc)
            if df == 0:
                continue
                
            # Inverse Document Frequency (IDF) - BM25 specific formulation
            # log( (N - DF + 0.5) / (DF + 0.5) + 1 )
            idf = np.log(((num_docs - df + 0.5) / (df + 0.5)) + 1.0)
            
            for i, doc in enumerate(corpus):
                tf = doc.count(term)
                if tf == 0:
                    continue
                    
                # TF Saturation and Document Length Normalization calculation
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_lengths[i] / avg_doc_len))
                
                scores[i] += idf * (numerator / denominator)
                
        return scores


if __name__ == "__main__":
    search_corpus = [
        ["the", "sun", "is", "bright", "and", "yellow"],          # Doc 0
        ["the", "sun", "is", "a", "star"],                        # Doc 1
        ["a", "black", "hole", "consumes", "all", "the", "light"] # Doc 2
    ]
    query = ["sun", "star"]
    
    engine = BM25Engine(k1=1.5, b=0.75)
    doc_scores = engine.compute_scores(query, search_corpus)
    
    assert doc_scores.shape == (3,)
    # Doc 1 contains both "sun" and "star" and is relatively short, so it should rank highest
    assert np.argmax(doc_scores) == 1
    # Doc 2 contains neither query word, score should be strictly zero
    assert doc_scores[2] == 0.0
    
    print(f"[TASK 03 PASSED] Okapi BM25 resolved accurately. Top Document Index: {np.argmax(doc_scores)}")