# Logic Breakdown: Euler Tour Tree Flattening
**Engineer:** Syed Saad Bin Irfan

## The Problem
Running calculations over subtrees (like summing all node values beneath a specific parent) usually requires traversing the tree recursively, which takes $O(N)$ linear time. To optimize this, we need a way to transform these structural paths into a flat layout that supports fast range lookups.

## My Approach
I implemented an **Euler Tour** structural flattening framework. By running a single Depth-First Search (DFS) pass, the engine tracks the exact entry and exit times of every node. 

The key optimization is that all descendants of a node are visited between that node's entry and exit steps. This maps an entire subtree into a continuous range within a flat array:

$$\text{Subtree}(V) \rightarrow \left[ \text{entry\_times}[V], \, \text{exit\_times}[V] \right]$$

This conversion allows you to plug the flattened array directly into high-speed structures like Segment Trees or Fenwick Trees, turning slow $O(N)$ tree operations into fast $O(\log N)$ range queries.

## Complexity Assessment
* **Flattening Runtime:** Linear $O(N)$ initialization pass.
* **Range Extraction Speed:** Instantaneous $O(1)$ boundaries lookup.
* **Memory Footprint:** $O(N)$ to hold the tracking metrics.