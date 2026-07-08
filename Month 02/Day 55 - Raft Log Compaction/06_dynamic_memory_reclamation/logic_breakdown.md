# Logic Breakdown: Dynamic Memory Reclamation
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Simply moving a pointer forward doesn't actually free up memory in languages like Python; references to old log entries can remain stuck in memory arrays, leading to resource leaks.

## My Approach
I utilized a list comprehension to build a new log array that explicitly filters out the old entries. This completely drops all references to the discarded items, allowing Python's garbage collector to immediately reclaim that memory.

## Complexity Profile
* Runtime Bounds: Filtering and copying the remaining items runs in linear time $O(L)$, where $L$ is the post-compaction log size.
* Space Constraints: Allocates memory for the kept entries, scaling at $O(L)$.