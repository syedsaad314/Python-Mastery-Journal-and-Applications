# Logic Breakdown: Process Lifecycles and Memory Isolation
**Engineer:** Syed Saad Bin Irfan

## The Problem
Developers transitioning from threading often assume global variables remain shared. Under a multiprocessing model, the operating system copies the entire process space (via `fork` or `spawn`), creating an independent interpreter environment where global changes do not cross process boundaries.

## My Approach
I created a script that explicitly targets a global list called `system_registry` from a child process. When the child appends data, it affects only its own isolated virtual address space. The parent's memory map remains completely unchanged, proving that structural isolation is maintained across OS processes.

## Complexity Profile
* **Runtime Bounds:** $O(1)$ allocation; process creation speed depends directly on OS system-call performance.
* **Space Constraints:** $O(M)$ where $M$ is a complete duplicate layout copy of the parent process's memory footprint.