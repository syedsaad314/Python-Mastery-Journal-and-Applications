# Logic Breakdown: Replicated State Machine Commit Loops
**Engineer:** Syed Saad Bin Irfan

## The Problem
Keeping logs uniform is only the first step. To keep the application state consistent across the cluster, nodes must execute commands against their local state machines in the exact same order up to the same commit line.

## My Approach
I built a **Sequential State Machine Commit Interface**.

The engine keeps an internal pointer, `last_applied_index`. When the cluster consensus moves the commit boundary forward, the state machine advances this pointer, reads the committed log entries sequentially, and parses them into mutations against a local key-value store. This ensures that every healthy node in the cluster reaches the exact same state.

## Complexity Profile
* **Runtime Bounds:** Processing commands takes $O(A)$ time, where $A$ is the number of unapplied entries being executed.
* **Space Constraints:** Memory scales linearly at $O(K)$ relative to the number of unique storage keys $K$ maintained in the dictionary.