# Logic Breakdown: Sinusoidal Positional Encoding
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Matrix multiplication ($QK^T$) is permutation-invariant. If you shuffle the words in a sentence, the Transformer yields the exact same attention outputs, rendering it completely "blind" to grammatical order and time.

## My Approach
I mapped absolute sequence positions into a geometric continuum using frequency bounds. I utilized interleaved Sine and Cosine waves mapped to specific dimension depths: $PE(pos, 2i) = \sin(pos / 10000^{2i/d})$, $PE(pos, 2i+1) = \cos(pos / 10000^{2i/d})$.
By adding these sinusoidal constants directly into the raw input embeddings, we embed a unique, mathematically determinable "spatial coordinate" into every word token, allowing the model to compute relative distances (e.g., word $A$ is 3 steps away from word $B$) using linear transformations.

## Complexity Profile
* Runtime Bounds: $O(N \cdot D)$ computed at optimal vector speeds via `np.sin` and `np.cos`.
* Space Constraints: $O(N \cdot D)$ to allocate the static lookup matrix.