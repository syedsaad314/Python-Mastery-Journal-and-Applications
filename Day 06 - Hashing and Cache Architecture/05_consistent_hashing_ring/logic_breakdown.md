# Logic Breakdown: Distributed Consistent Hashing Rings
**Engineer:** Syed Saad Bin Irfan

## The Problem
In distributed databases or horizontal caching setups, routing a key to a server using a simple modulo operation (`hash(key) % server_count`) creates a massive flaw. If one server goes offline or a new one is added, the `server_count` changes. This alters the result of the modulo operation for almost every key, causing a catastrophic cache miss storm that forces re-indexing across the entire cluster.

## My Approach
I built a virtual **Consistent Hashing Ring**. Both physical servers and data keys are hashed into a shared numerical integer space that forms a logical circle. To allocate a data entry, the engine hashes its key and walks clockwise along the ring until it hits the first available server position. I also implemented virtual replicas for each physical server, distributing them across multiple points on the ring to prevent data hot-spotting.

## Critical Thinking
*   **Time Complexity:** Adding or removing servers takes $O(V \log V)$ time due to array sorting needs. Finding the target server for a key uses a fast binary search (`bisect_right`), running in $O(\log V)$ time.
*   **Space Complexity:** Scales at $O(N \times V)$, tracking the total count of servers and their virtual replicas.

When a server node scales or fails, only a tiny fraction of the keys ($\frac{1}{N}$) need to be reassigned, keeping the rest of the cluster stable and running smoothly.