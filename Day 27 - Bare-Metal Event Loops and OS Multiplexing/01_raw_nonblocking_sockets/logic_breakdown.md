# Logic Breakdown: Raw Non-Blocking Sockets
**Engineer:** Syed Saad Bin Irfan

## The Problem
Standard network socket operations (like `accept()` or `recv()`) are blocking by default. They freeze the calling OS thread until external network traffic triggers a hardware wake-up call, which completely stops single-threaded execution loops.

## My Approach
I bypassed this bottleneck by using `server_sock.setblocking(False)`. This forces the operating system kernel to return immediately when a network call is made. 

If no incoming network data is queued in the kernel's internal ring buffers, the system throws an explicit `OSError` matching the `EAGAIN` or `EWOULDBLOCK` error codes. By safely trapping these specific exceptions, the execution pipeline can continue running other tasks instead of stalling.

## Complexity Profile
* **Runtime Bounds:** Immediate $O(1)$ polling evaluations.
* **Space Constraints:** Zero overhead $O(1)$ operational memory layout.