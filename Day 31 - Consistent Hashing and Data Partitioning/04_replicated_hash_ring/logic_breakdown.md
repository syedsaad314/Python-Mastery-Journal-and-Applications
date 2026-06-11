# Logic Breakdown: Replicated Consistent Hash Ring
**Engineer:** Syed Saad Bin Irfan

## The Problem
Consistent hashing handles where to put data, but if a node crashes, any data stored only on that machine is lost. To prevent data loss, systems need to replicate data across multiple backup servers without breaking the ring architecture.

## My Approach
I built a **Preference List Replication Router** into the hash ring.

When looking up a key, the router doesn't stop at the first node it finds. Instead, it continues walking clockwise around the ring to gather a list of distinct physical servers. Skipping any duplicate virtual nodes ensures the data is replicated across completely independent physical servers, protecting the system against single-node failures.

## Complexity Profile
* **Runtime Bounds:** Finding the replication chain takes $O(\log(N \cdot V) + R)$ time, where $R$ is the replication factor and $N \cdot V$ is the total number of virtual nodes on the ring.
* **Space Constraints:** Allocates $O(R)$ space to return the array list containing the destination target nodes.