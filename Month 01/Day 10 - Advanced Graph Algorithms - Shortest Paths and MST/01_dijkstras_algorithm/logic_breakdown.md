# Logic Breakdown: Dijkstra's Path Optimization
**Engineer:** Syed Saad Bin Irfan

## The Problem
When edges are paired with specific weights (like network latency or fuel consumption), a basic unweighted traversal will fail because it only counts the number of connections rather than their actual weights. To find the path with the true lowest total weight, we need an engine that systematically extracts the lowest-cost edge next.

## My Approach
I implemented **Dijkstra's Algorithm** utilizing Python’s internal `heapq` module to run a min-heap priority queue. The engine tracks the absolute minimum cost to reach each vertex. It continuously pops the cheapest unvisited node off the heap and runs a step called *relaxation* (updating a neighbor's path if this new route offers a lower total cost), which keeps routing calculations accurate and highly efficient.

## Critical Thinking
*   **Time Complexity:** Highly efficient at $O((V + E) \log V)$ when using a binary min-heap setup.
*   **Space Complexity:** Requires a straightforward $O(V + E)$ layout to maintain the graph mapping structures and tracking arrays.

This algorithm works perfectly for standard maps and data routing, but it can fail or get trapped in endless loops if any edge weights drop below zero.