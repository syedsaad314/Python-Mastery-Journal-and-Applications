# Logic Breakdown: Scaled Dot-Product Attention
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Recurrent architectures (RNN/LSTM) suffer from "information bottlenecks" because they pass sequence context sequentially through a single hidden vector. Distant words lose their signal.

## My Approach
I bypassed sequential processing entirely by engineering the Self-Attention primitive: $Attention(Q, K, V) = Softmax(\frac{QK^T}{\sqrt{d_k}})V$.
The dot product of Queries and Keys instantly calculates the "relevance" score between *every word* and *every other word* in the sequence simultaneously. The crucial addition is scaling by $\frac{1}{\sqrt{d_k}}$; without it, large dimensions push the dot products to extreme magnitudes, causing the Softmax to saturate and gradients to vanish.

## Complexity Profile
* Runtime Bounds: $O(N^2 \cdot D)$ where $N$ is sequence length and $D$ is dimension, bottlenecked by the $QK^T$ matrix multiplication.
* Space Constraints: $O(N^2)$ to store the explicit $N \times N$ attention probability weight matrix.