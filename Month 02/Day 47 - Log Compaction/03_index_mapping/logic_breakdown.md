# Logic Breakdown: Compacted Index Boundary Mapping
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Once historical logs are deleted during compaction, any newly joined or lagging node needs to know exactly where the history ends and where the snapshot's state data leaves off.

## My Approach
I engineered a dedicated metadata tracking mapping model. It captures the boundary markers (`last_included_index` and `last_included_term`) as fixed offset values. This gives the system a clear structural reference point to evaluate incoming cluster messages against, without needing the deleted logs.

## Complexity Profile
* Runtime Bounds: Executes instantly in constant $O(1)$ runtime bounds.
* Space Constraints: Uses a fixed, small metadata space allocation pattern of $O(1)$.