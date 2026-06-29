# Logic Breakdown: Vector Clock Pruning Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
As cluster topologies change, decommissioned nodes leave stale metadata behind in the vector maps. Over time, this causes the clock maps to grow without bound, wasting network bandwidth and memory.

## My Approach
I designed an active topology filter that cleans the clock maps. It cross-references keys against a verified list of active cluster members, dropping legacy fields to keep vector metadata lightweight.

## Complexity Profile
* Runtime Bounds: Runs in linear time $O(N)$ matching the length of the vector map.
* Space Constraints: Allocates memory at $O(A)$ for the filtered map, where $A$ is the count of active cluster nodes.