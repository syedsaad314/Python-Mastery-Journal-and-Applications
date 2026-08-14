# Logic Breakdown: Position-wise Feed-Forward Network
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Multi-Head Attention computes communication and context *between* tokens, but it only uses linear transformations. To model complex, non-linear realities, individual tokens require deeper non-linear mathematical processing before passing their new state up to the next layer.

## My Approach
I utilized a position-wise two-layer perceptron. Following standard Transformer architecture, the engine accepts an input vector (e.g., 512-dim), expands it out massively to a hidden projection (e.g., 2048-dim) via `W1`, applies a `ReLU` non-linearity to cull dead features, and compresses it back down to 512-dim via `W2`. Crucially, NumPy's broadcasted dot product applies these identical matrix weights across every token index equally in a single parallel step.

## Complexity Profile
* Runtime Bounds: $O(B \cdot N \cdot d_{model} \cdot d_{ff})$ determined by the heavy dimension expansion BLAS routines.
* Space Constraints: $O(B \cdot N \cdot d_{ff})$ temporary heap allocation to contain the massive uncompressed hidden state buffer.