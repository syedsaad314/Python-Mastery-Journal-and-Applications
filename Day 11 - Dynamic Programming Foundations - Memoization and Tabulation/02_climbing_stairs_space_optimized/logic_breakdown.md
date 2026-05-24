# Logic Breakdown: Linear Recurrence Space Optimizations
**Engineer:** Syed Saad Bin Irfan

## The Problem
While basic tabulation solves the subproblem calculation bottleneck by allocating an array of size $N$, keeping an entire history of values is often unnecessary. When a state transition equation only references its immediate predecessors, holding on to old historical values wastes precious system memory.

## My Approach
I optimized a linear combination problem by replacing the traditional full-sized array with two moving tracking variables: `one_step_back` and `two_steps_back`. As the processing loop advances, the variables overwrite obsolete history on the fly, calculating the target goal using only the values that matter right now.

## Critical Thinking
*   **Time Complexity:** Maintains an optimal linear $O(N)$ processing throughput.
*   **Space Complexity:** Drops down to a highly efficient constant $O(1)$ memory footprint.

This space-reduction approach is ideal for streaming data systems and low-memory embedded applications, cutting out array allocation bloat without sacrificing speed.