# Logic Breakdown: Node Churn Data Migration Analyzer
**Engineer:** Syed Saad Bin Irfan

## The Problem
When scaling a cluster up or down, we need to minimize data movement. Moving data over the network creates significant overhead and latency. We need a way to verify that our hash ring minimizes data rebalancing during cluster changes.

## My Approach
I built a **Migration Simulation Analyzer** to test data movement during a cluster scale-out event.

We map a static set of 2,000 keys across a 4-node cluster, then introduce a 5th node and measure how many keys change servers. With standard hashing, close to 80% of the keys would shift. Using consistent hashing with virtual nodes, the workload rebalances smoothly, moving only about 20% ($\frac{1}{N+1}$) of the total keys—confirming that the cluster minimizes network overhead during scaling.

## Complexity Profile
* **Runtime Bounds:** Evaluating the data movement scales linearly at $O(K \cdot \log(N \cdot V))$, running a binary search lookup for each of the $K$ tracking keys.
* **Space Constraints:** Requires $O(K)$ memory to track the initial state mappings of the keys during the test.