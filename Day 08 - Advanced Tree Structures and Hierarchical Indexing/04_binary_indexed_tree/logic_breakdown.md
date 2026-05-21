# Logic Breakdown: Binary Indexed Trees (Fenwick Ledgers)
**Engineer:** Syed Saad Bin Irfan

## The Problem
While Segment Trees handle range queries smoothly, they require substantial pointer overhead and up to four times the memory of the original array. For memory-constrained setups, tracking running totals or frequency counts across large indexes using heavy tree structures can quickly deplete available RAM.

## My Approach
I built a **Binary Indexed Tree** (Fenwick Tree). This architecture organizes running totals into a single, compact array by using clever bitwise math. By isolating the lowest set bit with the expression `index & (-index)`, the engine jumps precisely between nodes. This lets the system calculate cumulative prefixes and apply real-time updates with minimal pointer shifting.

## Critical Thinking
*   **Time Complexity:** Both prefix lookups and value updates execute in fast logarithmic time, $O(\log N)$.
*   **Space Complexity:** Highly memory-efficient at $O(N)$, requiring no extra node references or pointer tables.

This layout is perfect for building high-throughput packet counting tools and analytics dashboards, where you need fast, low-overhead summary calculations under tight memory limits.