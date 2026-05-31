# Logic Breakdown: Interoperating Blocking Functions
**Engineer:** Syed Saad Bin Irfan

## The Problem
If a third-party library or built-in file function executes a standard synchronous blocking call (like `time.sleep()` or `requests.get()`) inside an async function, it freezes the entire event loop, stalling all other active tasks.

## My Approach
I utilized `loop.run_in_executor()` to bridge the gap between synchronous and asynchronous code blocks. 

By offloading the blocking operation to a `ThreadPoolExecutor`, the system runs the synchronous task on a separate background thread. The primary event loop continues scheduling and running other tasks without lagging, allowing the application to handle legacy blocking operations cleanly.

## Complexity Profile
* **Runtime Bounds:** Task handoff runs in $O(1)$ time; execution speed matches the underlying thread performance.
* **Space Constraints:** Limited to a flat $O(W)$ tracking matrix size based on total background worker allocations.