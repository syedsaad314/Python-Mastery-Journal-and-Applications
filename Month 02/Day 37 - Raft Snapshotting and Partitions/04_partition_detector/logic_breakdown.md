# Logic Breakdown: Network Partition Connectivity Matrix
**Engineer:** Syed Saad Bin Irfan

## The Problem
To design resilient consensus engines, engineers must be able to test how systems handle partial network failures, such as a cluster splitting into competing majorities and minorities.

## My Approach
I built a **Network Partition Connectivity Matrix**.

This simulator uses an adjacency mapping layer to track packet paths. By isolating groups of nodes into disjoint reachability sets, we can realistically simulate network splits. This infrastructure allows us to test how candidate elections and replication loops behave when nodes are cut off from the rest of the cluster.

## Complexity Profile
* **Runtime Bounds:** Network connectivity checks execute in $O(1)$ constant time using hash set lookups.
* **Space Constraints:** Matrix storage maps scale at $O(N^2)$ relative to the total number of cluster nodes $N$.