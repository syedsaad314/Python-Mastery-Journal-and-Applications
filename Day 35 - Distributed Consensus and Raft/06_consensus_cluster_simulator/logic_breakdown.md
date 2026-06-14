# Logic Breakdown: Consensus Cluster Simulator Loop
**Engineer:** Syed Saad Bin Irfan

## The Problem
To guarantee data safety, a candidate cannot simply declare itself leader. It must collect verifiable approval from a strict majority of the cluster to ensure that no two nodes can claim leadership at the same time.

## My Approach
I engineered a **Consensus Cluster Simulator Loop** that calculates and enforces strict quorum majorities using the mathematical formula:

$$Q = \left\lfloor \frac{N}{2} \right\rfloor + 1$$

Where $N$ is the total number of nodes in the cluster. The simulator counts votes across all active peers, ensuring that a candidate can only step up to the leader role if its vote count meets or exceeds the quorum threshold $Q$. This rule prevents overlapping majorities and keeps the cluster safe from split-brain scenarios.

## Complexity Profile
* **Runtime Bounds:** Running the election loop scales linearly at $O(N)$ relative to the cluster size $N$.
* **Space Constraints:** Storage tracks at $O(N)$ space complexity to manage the cluster node mappings.