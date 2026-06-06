# Logic Breakdown: Generator Coroutine Suspension Mechanics
**Engineer:** Syed Saad Bin Irfan

## The Problem
Traditional function executions follow a strict sub-routine model—once invoked, they retain control of the thread until they run to completion, preventing other independent tasks from executing concurrently.

## My Approach
I utilized Python's generator mechanism (`yield`) to establish explicit, cooperative context-switching boundaries.

When a task encounters an unfulfilled network event, it yields control back to the driving scheduler along with a descriptive state tuple (e.g., `("read", fd)`). The runner intercepts this token and moves the task out of the active execution queue, freeing the single thread to run other operations while waiting for I/O readiness.

## Complexity Profile
* **Runtime Bounds:** Fast constant-time $O(1)$ context switching performance.
* **Space Constraints:** Minimal $O(1)$ memory state tracing overhead per frame instance.