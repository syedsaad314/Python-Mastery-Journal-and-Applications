# Logic Breakdown: Basic Consistent Hashing Ring
**Engineer:** Syed Saad Bin Irfan

## The Problem
When using simple remainder-based hashing ($hash(k) \pmod N$), changing the value of $N$ shifts almost every key to a completely different node. In a production caching cluster, this causes an immediate cache miss storm, spiking database load.

## My Approach
I built a continuous **Consistent Hashing Ring** mapped across a 32-bit numerical space. 

Both the processing servers and the data keys are hashed using the same MD5 hashing function. To find which server handles a key, we hash the key and walk clockwise along the ring until we hit the first server position. I used the `bisect` library to run a binary search over the sorted array of node locations, ensuring fast lookups even as the system scales up.

## Complexity Profile
* **Runtime Bounds:** Server lookups execute in $O(\log N)$ logarithmic time via binary search, where $N$ is the count of nodes. Adding or removing a node runs in $O(N)$ due to array shifting during sorted insertions.
* **Space Constraints:** Scales linearly at $O(N)$ to keep tracking records for each node's position.