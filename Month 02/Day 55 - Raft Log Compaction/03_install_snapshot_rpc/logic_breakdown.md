# Logic Breakdown: InstallSnapshot RPC Payloads
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When a follower falls too far behind (e.g., due to a long network partition), the leader may have already compacted and discarded the entries that follower needs. The standard `AppendEntries` RPC will fail indefinitely because the leader no longer has the history to back up and find a common match point.

## My Approach
I designed an `InstallSnapshot` RPC payload. Instead of sending a stream of individual delta entries, this message allows the leader to package its entire compiled state data structure and send it over the network in a single operation.

## Complexity Profile
* Runtime Bounds: Copying the state dictionary runs in $O(S)$ time, where $S$ is the number of keys in the state.
* Space Constraints: Allocates memory linearly at $O(S)$ to hold the payload copy.