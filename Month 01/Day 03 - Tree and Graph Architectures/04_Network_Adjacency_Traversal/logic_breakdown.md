# Logical Breakdown: Network Adjacency Traversal

### The Problem
Relationships in real-world data—such as financial transactions, user interactions, or fraud networks—are non-linear and web-like. To analyze these patterns, we need graph processing systems that traverse connected paths without getting trapped in infinite loops when encountering structural cycles.

### Architectural Thought Process
I implemented an adjacency map layout using explicit hash sets, preventing duplicate edge mappings and enabling constant-time connection lookups. The graph engine uses distinct algorithmic approaches: Breadth-First Search (BFS) uses a queue to evaluate immediate proximity zones, while Depth-First Search (DFS) uses a stack to trace deep structural paths first. Both approaches cross-reference an explicit tracking set (`visited_registry`) to process cyclical paths safely.

### Complexity & Scope
*   **Time Complexity:** Both graph search algorithms operate at $O(V + E)$ efficiency over node networks.
*   **AI/ML Real-world Application:** Provides the direct algorithmic foundation for mapping social graphs, executing fraud detection cascades, and structuring modern Knowledge Graphs.