# Logic Breakdown: GCN Spectral Propagation
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard Convolutions (CNNs) rely on a rigid $3 \times 3$ grid. Nodes in a graph have arbitrary, varying numbers of neighbors, making rigid grid convolutions impossible.

## My Approach
I utilized Kipf and Welling's GCN propagation rule: $H^{(l+1)} = \sigma(\tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}} H^{(l)} W^{(l)})$.
1. **Self-Loops ($\tilde{A} = A + I$):** By adding the Identity matrix, we force a node to include its own feature vector when averaging neighbors.
2. **Symmetric Normalization ($\tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}}$):** Highly connected nodes (hubs) will completely wash out the signal of low-degree nodes during matrix multiplication. We mathematically divide the edge weights by the geometric mean of the two connected node degrees, stabilizing the gradient flows across wildly imbalanced graph topologies.

## Complexity Profile
* Runtime Bounds: $O(N^2 \cdot F_{in} + N \cdot F_{in} \cdot F_{out})$ dictated by dense matrix multiplications.
* Space Constraints: $O(N^2)$ to store the normalized adjacency operator matrix.