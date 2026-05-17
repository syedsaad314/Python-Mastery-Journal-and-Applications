# Logical Breakdown: Min-Max Binary Heap Priority Queue

### The Problem
Sorting an entire dataset repeatedly to extract the highest or lowest priority items creates performance bottlenecks. Real-time tasks—such as executing best-first search operations or processing continuous data queues—require data structures that can ingest items and retrieve the top-priority value with minimal performance overhead.

### Architectural Thought Process
I implemented a complete binary min-heap mapped inside a standard flat array. Index arithmetic formulas locate relational nodes instantly without requiring full pointer node objects. When an element is removed from the top, the last item shifts to the root position and cascades downward through comparisons (`sift_down`), keeping the tree balanced without sorting the entire array.

### Complexity & Scope
*   **Time Complexity:** Updates (`push`) and extractions (`pop`) run at a logarithmic scale of $O(\log N)$, while reading the top element takes constant $O(1)$ time.
*   **AI/ML Real-world Application:** Provides the direct underlying engine for pathfinding routines (like A* and Dijkstra), operational priority scheduling, and automated data loaders.