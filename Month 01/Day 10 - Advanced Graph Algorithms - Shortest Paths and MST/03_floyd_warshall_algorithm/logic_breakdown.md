# Logic Breakdown: Floyd-Warshall Matrix Solver
**Engineer:** Syed Saad Bin Irfan

## The Problem
When building comprehensive routing maps for transit networks or backend systems, running single-source algorithms over and over for every single node is highly inefficient. We need a clean, structured way to evaluate, update, and build an all-to-all distance map across every node pair in a single coordinated operation.

## My Approach
I utilized the **Floyd-Warshall Algorithm**, a multi-layered dynamic programming strategy that works directly with adjacency matrices. The engine uses three nested loops to test every pair of nodes $(i, j)$ and check if routing through an intermediate node $k$ reduces the total path cost. If $dist[i][k] + dist[k][j] < dist[i][j]$, the matrix updates instantly with the new, more efficient value.

## Critical Thinking
*   **Time Complexity:** Enforced at a strict cubic $O(V^3)$ threshold because of its three nested loops.
*   **Space Complexity:** Locked in at a stable quadratic $O(V^2)$ size to maintain the distance tracking matrix.

This dense, matrix-based approach is ideal for small-to-medium networks that require quick, continuous path lookups without running fresh searches each time.