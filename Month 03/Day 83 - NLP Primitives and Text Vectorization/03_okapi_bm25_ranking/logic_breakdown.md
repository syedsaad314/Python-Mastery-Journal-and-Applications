# Logic Breakdown: Okapi BM25 Ranking
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard TF-IDF has two flaws for Search Engines:
1. **No TF Saturation:** If "data" appears 10 times in Doc A and 100 times in Doc B, TF-IDF makes Doc B 10x more relevant, which is mathematically excessive.
2. **Length Bias:** Long documents naturally contain more matches simply by virtue of length, unfairly pushing down dense, highly relevant short documents.

## My Approach
I encoded the **Okapi BM25** search ranking formula. 
1. **$k_1$ parameter (Saturation):** Caps the impact of Term Frequency. Once a term appears a few times, seeing it again yields diminishing returns.
2. **$b$ parameter (Length Normalization):** Penalizes documents that are longer than the corpus average length (`avg_doc_len`). If a document is long, its TF is strictly discounted in the denominator, forcing long documents to prove their relevance denser than short ones to rank equally.

## Complexity Profile
* Runtime Bounds: $O(Q \cdot D \cdot W)$ evaluating $Q$ query terms across $D$ documents of length $W$.
* Space Constraints: $O(D)$ maintaining the resultant ranking scores per document.