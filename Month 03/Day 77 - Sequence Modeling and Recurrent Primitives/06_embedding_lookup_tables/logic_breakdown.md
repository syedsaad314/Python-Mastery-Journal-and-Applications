# Logic Breakdown: Dense Embedding Lookup Tables
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Passing categorical data (like NLP tokens) into networks requires One-Hot Encoding (a vector of 10,000 zeros and a single 1). Executing an Affine Transform `np.dot(One_Hot, Weights)` performs 10,000 floating-point multiplications, 9,999 of which explicitly evaluate to zero—wasting extreme processing power.

## My Approach
I bypassed matrix multiplication entirely using an Array Index Lookup. Mathematically, dotting a one-hot vector against a weight matrix perfectly isolates a single row. Therefore, I map categorical integers directly into the row boundaries of a dense embedding matrix `E_matrix[word_indices]`. This fetches the correct dense semantic vector natively in C-level array memory in $O(1)$ time without any mathematical operations.

## Complexity Profile
* Runtime Bounds: True deterministic $O(S)$ where $S$ is the sequence length of integer indices.
* Space Constraints: $O(V \cdot D)$ persistent RAM footprint for the lookup dictionary ($V$ = Vocab Size, $D$ = Dimension).