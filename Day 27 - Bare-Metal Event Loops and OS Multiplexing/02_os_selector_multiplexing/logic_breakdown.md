# Logic Breakdown: OS Selector Event Multiplexing
**Engineer:** Syed Saad Bin Irfan

## The Problem
Continuously polling non-blocking sockets in a raw loop creates high CPU usage, wasting processing cycles as the thread rapidly checks for data that hasn't arrived yet.

## My Approach
I implemented a structural multiplexing model using Python's `selectors.DefaultSelector`. 

This delegate hooks directly into low-level operating system notification engines, like Linux `epoll` or macOS `kqueue`. Sockets are registered with the selector along with a target event mask (`EVENT_READ`). When `selector.select()` runs, the calling thread is suspended until the OS kernel handles the underlying network event, allowing for highly efficient, event-driven single-threaded scaling.

## Complexity Profile
* **Runtime Bounds:** $O(1)$ event notifications on modern kernels via epoll/kqueue.
* **Space Constraints:** $O(N)$ memory mapping relative to total tracked file descriptors.