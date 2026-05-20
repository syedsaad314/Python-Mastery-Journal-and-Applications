# Logic Breakdown: Probabilistic Bloom Filter Metrics
**Engineer:** Syed Saad Bin Irfan

## The Problem
When scanning millions of incoming requests (like malicious URLs or missing usernames), checking a standard hash set uses too much memory under heavy load. If the dataset scales to billions of items, keeping it entirely in RAM is impossible. We need a memory-efficient filter that can intercept requests and weed out absolute misses before hitting slow disk storage.

## My Approach
I built a **Bloom Filter** using a compact bit array paired with a multi-salt hash generator. When an item is added, it passes through several salted hashing cycles, and the bits at those calculated index points are flipped to `1`. 

## Critical Thinking
This setup introduces a unique probabilistic behavior:
*   If any of the calculated bits are `0`, the item is **guaranteed to be absent** (Zero False Negatives).
*   If all bits are `1`, the item **might be present**, but there's a small chance of a false positive caused by separate hashes overlapping on the same bits.

*   **Time Complexity:** Operations run in constant time at $O(K)$, where $K$ tracks the number of hashing cycles, completely independent of total items stored.
*   **Space Complexity:** Uses a fixed footprint of $O(M)$ bits, saving over 90% more RAM than traditional string hash sets.

This pattern is widely used in front-end database routing (like BigTable and Cassandra) to shield physical disk drives from useless query lookups.