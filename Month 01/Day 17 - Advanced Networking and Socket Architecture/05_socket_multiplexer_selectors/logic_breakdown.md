# Logic Breakdown: Non-Blocking I/O Multiplexing
**Engineer:** Syed Saad Bin Irfan

## The Problem
Spawning a new system thread or process for every incoming user connection quickly strains server memory, leading to major scaling performance bottlenecks.

## My Approach
I utilized Python's low-level `selectors` framework to build a single-threaded architecture capable of managing multiple connections concurrently.

The server configures all incoming sockets as non-blocking (`setblocking(False)`). Instead of getting stuck waiting for a specific connection to receive data, it registers all sockets with an OS-level polling mechanism (like `epoll` or `select`). The main loop continuously checks for active network events, processing incoming data only when a socket is ready to read, maximizing performance within a single process.

## Complexity Profile
* **Runtime Bounds:** Controlled at $O(1)$ event loop cycles per ready network state.
* **Space Constraints:** Scaled smoothly at $O(C)$ relative to total concurrent open file handles.