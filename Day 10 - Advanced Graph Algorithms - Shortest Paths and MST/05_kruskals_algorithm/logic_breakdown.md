# Logic Breakdown: Kruskal's Edge Sorting
**Engineer:** Syed Saad Bin Irfan

## The Problem
For sparse graphs spread across vast distances (such as regional pipeline layouts or distributed networks), tracking connections node-by-node can create unnecessary overhead. We need an alternative approach that looks at connections globally, evaluating the cheapest overall links first while ensuring they don't form any closed loops.

## My Approach
I implemented **Kruskal's Algorithm**, an edge-centric MST strategy. The engine first flattens and sorts every edge in the entire graph by weight. It then loops through these sorted edges, using an internal Disjoint Set Union (DSU) structure to check if the two connected nodes are already part of the same tree. If they are in different groups, the engine merges them safely, ensuring the tree grows efficiently without ever forming a loop.

## Critical Thinking
*   **Time Complexity:** Dominated by the initial sorting stage, scaling smoothly at $O(E \log E)$.
*   **Space Complexity:** Bounded efficiently at $O(V + E)$ to maintain tracking arrays and trees.

This edge-centric global sort approach works exceptionally well on sparse graphs, making it a reliable tool for wide-area network design.