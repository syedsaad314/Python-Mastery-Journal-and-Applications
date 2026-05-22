# Logic Breakdown: Bellman-Ford Routing Mechanics
**Engineer:** Syed Saad Bin Irfan

## The Problem
Dijkstra's algorithm breaks down when a graph contains negative edge weights because it locks in path costs prematurely. Even worse, if a graph contains a *negative cycle* (a loop whose total weight adds up to less than zero), an algorithm could loop infinitely, reducing the path cost forever. We need an engine that can safely compute paths with negative weights and explicitly flag these infinite loops.

## My Approach
I built a **Bellman-Ford Engine** that processes graphs by systematically relaxing every single edge in the network $V - 1$ times, where $V$ represents the total number of vertices. Since the longest possible simple path across a graph uses $V - 1$ edges, costs stabilize by the final pass. The engine then runs one more full pass; if any cost drops further during this extra check, it means a negative cycle exists, and the engine throws an explicit error.

## Critical Thinking
*   **Time Complexity:** Runs in a slower $O(V \times E)$ time due to its brute-force relaxation sweeps.
*   **Space Complexity:** Highly memory-efficient at $O(V)$ to track the distance matrix.

While it is slower than heap-based choices, its ability to detect negative cycles makes it essential for financial arbitrage engines and complex distance-vector routing protocols.