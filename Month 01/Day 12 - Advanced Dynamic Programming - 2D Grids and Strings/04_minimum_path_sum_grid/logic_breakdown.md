# Logic Breakdown: Spatial Path Summation
**Engineer:** Syed Saad Bin Irfan

## The Problem
When routing through a 2D environment where each cell carries a latency or travel cost (like an AI navigating a map), DFS or simple recursion will result in astronomical execution times evaluating dead ends. We need to lock in the cheapest way to reach every single cell as we move forward.

## My Approach
I utilized an **In-Place Grid Modification** strategy. Since you can only move right or down, the edges of the grid are bottlenecks—the top row can only be reached from the left, and the left column only from above. I pre-calculated these border costs. For the inner cells, the engine dynamically updates each node by adding its own value to the minimum of its top or left neighbor. By the time it hits the bottom right, it holds the absolute minimal cost.

## Critical Thinking
*   **Time Complexity:** Fast $O(R \times C)$ grid scan.
*   **Space Complexity:** $O(R \times C)$ matrix allocation, though this specific implementation performs an intentional deep-copy.

This maps perfectly to logistical movement tracking and latency optimization in distributed matrices.