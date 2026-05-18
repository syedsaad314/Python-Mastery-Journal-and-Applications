# Logical Breakdown: AVL Tree Engine

### The Problem
Standard Binary Search Trees (BST) perform efficiently when items are inserted in random order. However, if data arrives already sorted (e.g., incremental time series logs), a standard tree appends every item to the same side, degenerating into a slow, linear $O(N)$ linked chain that defeats the purpose of tree indexing.

### Architectural Thought Process
I implemented a self-balancing AVL tree architecture. Each node tracks its current branch height. After a new value is inserted recursively, the engine computes balance factors at each step. If a branch's height profile shifts out of balance (balance factor $> 1$ or $< -1$), the engine performs precise left or right pointer modifications (`rotate_left`/`rotate_right`), restoring a balanced shape.

### Complexity & Scope
*   **Time Complexity:** Guarantees lookup, insertion, and deletion metrics scale at a strict logarithmic level of $O(\log N)$ by maintaining tree balance.
*   **AI/ML Real-world Application:** Demonstrates the core balancing logic used in relational database indexes, system memory maps, and high-frequency key-value storage engines.