# Logic Breakdown: Heavy-Light Tree Decomposition
**Engineer:** Syed Saad Bin Irfan

## The Problem
Querying or updating values along an arbitrary path between two tree nodes typically scales with the tree's height, running in $O(N)$ linear time. To optimize this, we need a method to organize paths into continuous linear blocks that support fast bulk updates and range lookups.

## My Approach
I implemented a **Heavy-Light Decomposition (HLD)** engine. This framework breaks down a tree structure into distinct paths using a two-pass classification strategy:

1. **Heavy Assessment Pass:** For each node, it counts the size of its child subtrees. The edge leading to the largest child subtree is classified as a **Heavy Edge**, while all other branching choices become **Light Edges**.
2. **Stitching Pass:** It traverses the tree, prioritizing the heavy edges to group them into continuous segments inside a flat array.

(0)
   //  \      [ // = Heavy Path Chain (Continuous Array Indices) ]
  (1)  (2)    [  \ = Light Branch Edge Offset ]
 //
(3)

Because paths are grouped into continuous array intervals, querying values along a path can be broken down into a series of range queries. As you traverse up towards a common ancestor, you jump across path heads in logarithmic time.

## Complexity Evaluation
* **Decomposition Pass:** Linear $O(N)$ setup time.
* **Path Interrogation Queries:** Bounded strictly at **$O(\log^2 N)$** steps by jumping across path components.
* **Space Overhead Profiles:** $O(N)$ memory allocation steps.

This architecture is ideal for handling network routing traffic metrics, variable coordinate pipelines, and dynamic tree updates.