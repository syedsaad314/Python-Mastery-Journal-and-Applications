# Logic Breakdown: TF-IDF Vectorization
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Bag-of-Words (BoW) counting dominates semantic meaning with structural grammar. A document full of the word "the" will mathematically overwhelm specific, meaning-dense words like "quantum" during vector similarity comparisons.

## My Approach
I utilized the **TF-IDF (Term Frequency - Inverse Document Frequency)** mathematical heuristic. 
1. **TF:** Counts how often a term appears locally in a document.
2. **IDF:** Penalizes words that appear globally across the entire dataset. The equation $\log(\frac{N}{1 + DF}) + 1$ aggressively squashes the weight of stop-words. 
3. Finally, multiplying the two and applying $L2$ Normalization directly guarantees that vectors map onto a unit hypersphere, making document length irrelevant and Cosine Similarity computations stable.

## Complexity Profile
* Runtime Bounds: $O(D \cdot W \cdot V)$ where $D$ is docs, $W$ is words per doc, and $V$ is vocab length.
* Space Constraints: $O(D \cdot V)$ static dense matrix allocation.