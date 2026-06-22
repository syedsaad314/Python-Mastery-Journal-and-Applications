# Logic Breakdown: Prim's Minimum Spanning Tree
**Engineer:** Syed Saad Bin Irfan

## The Problem
When laying physical infrastructure (like fiber-optic cables or power grids), you need to connect all locations safely without creating loops, while keeping total installation costs as low as possible. This requires extracting a **Minimum Spanning Tree (MST)** from a complex web of potential connections.

## My Approach
I built a node-focused **Prim's Algorithm** engine that uses a min-heap priority queue. Starting from an initial seed node, the engine logs all outgoing connections and greedily selects the absolute cheapest edge leading to an unvisited destination. Once that new node is verified, its own outgoing edges join the priority queue, expanding the tree layout safely without ever forming loops.

## Critical Thinking
*   **Time Complexity:** Operates at $O((V + E) \log V)$ using binary min-heap adjustments.
*   **Space Complexity:** Uses $O(V + E)$ space to hold active edges within the priority queue structures.

This node-expanding approach is highly effective for dense graphs that feature many cross-connections, quickly isolating the optimal structural backbone.