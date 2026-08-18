# Logic Breakdown: Spatial Message Passing (MPNN)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Spectral GCNs operate heavily on the entire graph topology simultaneously using Laplacian eigenvector approximations, making them extremely inflexible when handling directed graphs or dynamic graphs where edges change rapidly.

## My Approach
I stripped Graph Processing down to its fundamental spatial primitives: **Message Passing Neural Networks (MPNN)**.
Instead of relying on the global graph Laplacian, the algorithm operates locally. 
1. Nodes calculate outbound mathematical messages via `W_msg`. 
2. We utilize `np.dot(A, messages)` to naturally sum incoming messages, enforcing the physical boundaries of the adjacency matrix edges. 
3. Finally, the node concatenates its original identity with its new neighborhood context and updates its state. This spatial formulation works flawlessly on directed, unseen, or evolving graph topologies.

## Complexity Profile
* Runtime Bounds: $O(|E| \cdot F + N \cdot F^2)$ scaling linearly with the number of Physical Edges $|E|$ rather than $N^2$ if optimized with sparse matrices.
* Space Constraints: $O(N \cdot F)$ dynamic state matrices.