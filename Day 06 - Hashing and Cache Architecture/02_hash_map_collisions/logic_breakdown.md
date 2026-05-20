# Logic Breakdown: Manual Hash Maps & Collision Resolution
**Engineer:** Syed Saad Bin Irfan

## The Problem
High-level languages handle dictionaries under the hood, masking the core issue of memory distribution. Because storage arrays are finite, distinct string keys inevitably hash to the same memory index slot. Without clear collision management, conflicting records will overwrite each other.

## My Approach
I implemented a manual hash table utilizing the **Chaining** design pattern. The underlying architecture is an array of lists. When multiple keys map to the exact same index, their key-value pairs are stored together within that bucket list. To distribute entries uniformly, I used a polynomial string rolling calculation multiplied by a prime constant ($31$).

## Critical Thinking
*   **Time Complexity:** In optimal scenarios, lookup takes $O(1)$. If the hash function breaks down and clusters all records into a single index, performance drops to a linear search of $O(N)$.
*   **Space Complexity:** Scales at $O(B + N)$, tracking both initialized bucket slots ($B$) and active data elements ($N$).

This pattern shows the importance of selecting high-quality hash functions to prevent slow operations in primary database engines.