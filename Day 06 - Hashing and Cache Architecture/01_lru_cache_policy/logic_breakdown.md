# Logic Breakdown: Least Recently Used Cache Structure
**Engineer:** Syed Saad Bin Irfan

## The Problem
When a web app or machine learning service pulls data repeatedly from a persistent database, performance tanks due to IO overhead. Using a simple array-based cache means evicting old elements requires shifting items in memory, which runs in slow linear time. I need a cache that reads, inserts, and updates expiration states in absolute constant time.

## My Approach
I paired a native dictionary with a custom doubly linked list. The dictionary maps keys directly to individual nodes in the linked list, allowing instant lookups. The doubly linked list maintains the precise order of use without needing item shifts. Sentinel nodes (`head` and `tail`) were added to the list edges to avoid complex null pointer checks during node separation.

## Critical Thinking
This design achieves strict constant time performance for all core actions:

*   **Time Complexity:** Lookups run at $O(1)$ and additions/evictions run at $O(1)$.
*   **Space Complexity:** Scales linearly at $O(C)$ where $C$ represents the fixed maximum capacity boundary.

This pattern is a staple for high-speed API token management and deep learning model weights caching, where keeping hot assets available in RAM is non-negotiable.