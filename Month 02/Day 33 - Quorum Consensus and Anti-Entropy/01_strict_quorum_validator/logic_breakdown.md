# Logic Breakdown: Strict Quorum Consensus Validator
**Engineer:** Syed Saad Bin Irfan

## The Problem
In masterless distributed storage layers, updates are sent to multiple replicas concurrently. If a client reads from a set of nodes without overlapping with the nodes that processed the last write, the client will receive stale data.

## My Approach
I implemented a **Quorum Configuration Validator** that models cluster survival properties using the mathematical equation:

$$R + W > N$$

Where $N$ is the replication factor, $W$ is the minimum write confirmations required, and $R$ is the minimum read nodes sampled. By ensuring the combined size of the write set and read set is strictly greater than the total number of replicas, the Pigeonhole Principle guarantees that at least one node in the read sample contains the most recent write.

## Complexity Profile
* **Runtime Bounds:** Validation checks execute in $O(1)$ constant mathematical execution time.
* **Space Constraints:** Requires $O(1)$ auxiliary memory space to track scalar properties.