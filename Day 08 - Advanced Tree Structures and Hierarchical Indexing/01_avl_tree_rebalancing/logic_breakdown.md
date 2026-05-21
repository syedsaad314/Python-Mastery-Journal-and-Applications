# Logic Breakdown: AVL Self-Balancing Architectures
**Engineer:** Syed Saad Bin Irfan

## The Problem
Standard Binary Search Trees (BST) work beautifully for search operations under mixed workloads. However, if the incoming data stream arrives pre-sorted (e.g., incremental primary keys or sorted timestamps), a basic BST degrades into a linear single-linked list. This drops performance from fast logarithmic operations down to slow linear processing times.

## My Approach
I implemented a strict **AVL Tree** structure. Each node monitors its internal `height` metric. Every time a new key is added, the system checks the balance factors along the execution path. If any node's left and right subtrees differ in height by more than $1$, the system fires targeted pointer swaps—using single (`rotate_left`/`rotate_right`) or double combinations—to pull the tree back into absolute balance.

## Critical Thinking
*   **Time Complexity:** Guarantees strict search, insertion, and deletion execution runtimes at $O(\log N)$, completely neutralizing worst-case structural skewing.
*   **Space Complexity:** Consumes $O(N)$ space to store tree values and height properties within memory.

This approach prevents bad performance traps in memory indexes, ensuring predictable lookups even under highly skewed or pre-sorted input streams.