# Logic Breakdown: Centroid Decomposition Tree Balancing
**Engineer:** Syed Saad Bin Irfan

## The Problem
When trees grow highly unbalanced or skewed (like a single long chain of nodes), typical $O(\log N)$ path algorithms degrade down to an inefficient $O(N)$ linear runtime. We need a way to restructure skewed trees into a balanced hierarchy to ensure predictable, fast operations.

## My Approach
I built a **Centroid Decomposition** divide-and-conquer framework. This engine systematically finds a **Centroid** node—a structural center point whose removal splits the tree into subcomponents that contain at most $N/2$ nodes.

Once the centroid is identified, it is disconnected from the tree, and the algorithm repeats recursively on the remaining isolated subcomponents. This restructures the original tree layout into a balanced tracking tree.

This restructuring bounds the maximum depth of the centroid tree to exactly $O(\log N)$, guaranteeing consistent performance regardless of how unbalanced the initial input data was.

## Complexity Assessment
* **Decomposition Processing:** Bounded at $O(N \log N)$ total time.
* **Balanced Height Limit:** Guaranteed max path depth of $O(\log N)$.
* **Space Requirements:** Requires $O(N)$ memory space to preserve tracking metrics.