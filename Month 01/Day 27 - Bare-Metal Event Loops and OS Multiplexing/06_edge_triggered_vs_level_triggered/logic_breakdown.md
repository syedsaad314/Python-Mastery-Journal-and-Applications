# Logic Breakdown: Edge-Triggered vs Level-Triggered Notification Modes
**Engineer:** Syed Saad Bin Irfan

## The Problem
In edge-triggered polling modes (like `epoll` with `EPOLLET`), the operating system kernel triggers an event notification only when new data actively hits the hardware interface. If your application code reads only a portion of the incoming packet buffer and exits, it will stall, as the kernel won't trigger another notification for the data left behind.

## My Approach
I implemented a robust socket-draining pattern to ensure clean data processing in edge-triggered environments.

The parsing engine wraps network reads in an aggressive `while True` loop that continuously pulls chunks out of the socket's kernel queue. The loop runs until the network call encounters an explicit `EAGAIN` or `EWOULDBLOCK` exception signal, indicating the underlying buffer has been completely drained. This pattern guarantees all pending data is extracted, preventing event starvation issues.

## Complexity Profile
* **Runtime Bounds:** Runs in linear $O(M)$ time relative to total inbound buffer sizes.
* **Space Constraints:** Scales linearly at an $O(M)$ rate to aggregate incoming stream parts.