# Logic Breakdown: Memory-Mapped Feather File I/O
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Reading multi-gigabyte files into application memory forces full heap allocation spikes and disk read wait states, crashing systems with constrained physical RAM.

## My Approach
I used `pa.memory_map()` with PyArrow's Feather reader. The OS kernel maps the file on disk directly into the virtual address space of the process. Pages are lazy-loaded on-demand via system page faults, letting application logic access huge tables without copying entire files into RAM.

## Complexity Profile
* Runtime Bounds: $O(1)$ file open time; $O(K)$ lazy page loading bounds where $K$ is accessed data size.
* Space Constraints: $O(1)$ resident memory footprint prior to reading pages.