# Logic Breakdown: State Machine Driver Execution
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Logs are just mid-flight records until they are executed. To make the consensus engine useful, we must reliably feed these committed logs into an actual storage layer without running any command twice.

## My Approach
I implemented a catch-up loop that tracks execution with a specialized pointer (`last_applied`). The loop advances whenever the `commit_index` outpaces the application pointer, applying each command sequentially to the underlying key-value dictionary.

## Complexity Profile
* Runtime Bounds: Processing caught-up logs runs in $O(K)$ time, where $K$ is the number of newly committed logs.
* Space Constraints: Operates inline, requiring $O(1)$ constant overhead.