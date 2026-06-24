# Logic Breakdown: Log Garbage Collection
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
After persisting a system snapshot image safely to disk, keeping the old log records in RAM wastes memory and slows down array traversal operations.

## My Approach
I engineered a filtering garbage collection sweep. It loops over the active log array and retains only the entries whose index markers sit strictly past the snapshot index ceiling, freeing up memory while keeping newer uncommitted entries untouched.

## Complexity Profile
* Runtime Bounds: Runs in linear $O(L)$ execution bounds relative to original log length $L$.
* Space Constraints: Generates a optimized filtered list map holding remaining indices at $O(R)$ remaining records.