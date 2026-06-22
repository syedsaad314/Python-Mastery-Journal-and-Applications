# Logic Breakdown: OS Signal Interception and Child Process Rollbacks
**Engineer:** Syed Saad Bin Irfan

## The Problem
When an orchestration layer scales down, it sends terminal signals like `SIGTERM` to worker nodes. If a child process gets killed mid-write, it can leave databases locked or output files half-written and corrupted.

## My Approach
I set up an explicit signal handling pipeline inside the child process using Python's core `signal` engine. 

By intercepting the OS `signal.SIGTERM` dispatch, the default abrupt exit handler is overridden. When a shutdown request is received, the application captures it and runs an atomic rollback procedure first, ensuring data integrity before calling a clean `sys.exit(0)`.

## Complexity Profile
* **Runtime Bounds:** Constant $O(1)$ signal interception and validation mechanics.
* **Space Constraints:** Constant $O(1)$ structural memory footprints throughout execution.