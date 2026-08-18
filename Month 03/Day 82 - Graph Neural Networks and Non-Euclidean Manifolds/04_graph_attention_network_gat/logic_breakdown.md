# Logic Breakdown: Graph Attention Masking (GAT)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard GCNs treat all neighbor nodes identically, averaging their features equally. In reality, some neighbors (e.g., a direct supervisor in a social graph) carry vastly more semantic importance than others (e.g., a distant acquaintance).

## My Approach
I fused Transformer Self-Attention with spatial graph topologies. The network computes an attention score between every possible pair of nodes. 
However, standard attention is $O(N^2)$ dense. I utilized `np.where(mask > 0, attention_scores, -1e9)`. By masking out any pairs that do not share a physical physical edge in the Adjacency Matrix ($A$), the Softmax probability drops to zero for non-neighbors. The node dynamically learns *which specific neighbors* to pay attention to during message aggregation.

## Complexity Profile
* Runtime Bounds: $O(N^2 \cdot F)$ for dense loop demonstration, practically optimized to $O(|E| \cdot F)$ using sparse tensor indices.
* Space Constraints: $O(N^2)$ to compute the unmasked pairwise concatenated combinations.