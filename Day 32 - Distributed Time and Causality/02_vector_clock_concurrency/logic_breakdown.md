# Logic Breakdown: Vector Clocks Concurrency Analyzer
**Engineer:** Syed Saad Bin Irfan

## The Problem
While Lamport timestamps can order events linearly, they cannot identify when events happen **concurrently** (meaning two events occurred independently without knowledge of one another). To detect write conflicts in multi-master setups, we need to capture full causal history.

## My Approach
I upgraded the logical clock framework to a **Vector Clock Engine**.

Instead of a single integer, every node maintains an internal dictionary (a vector) mapping every active server to its latest known logical counter. 
* To prove state $X$ structurally directly preceded state $Y$, every entry in vector $X$ must be less than or equal to the corresponding entry in vector $Y$, with at least one entry being strictly smaller.
* If neither vector dominates the other (e.g., node A has a higher counter in one vector, but node B has a higher counter in the other), the engine flags the relationship as a `CONCURRENT_CONFLICT`.

## Complexity Profile
* **Runtime Bounds:** Vector merges and comparisons run in $O(N)$ linear time, where $N$ represents the total number of unique nodes tracked in the cluster.
* **Space Constraints:** Memory scales linearly at $O(N)$ to store the tracking map vectors.