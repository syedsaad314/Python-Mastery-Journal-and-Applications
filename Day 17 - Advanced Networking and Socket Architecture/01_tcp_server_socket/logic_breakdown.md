# Logic Breakdown: Low-Level TCP Socket Architecture
**Engineer:** Syed Saad Bin Irfan

## The Problem
High-level libraries mask what happens under the hood when a network interface establishes a socket. We need a way to directly configure raw network resources and handle explicit incoming streams safely.

## My Approach
I built a direct object wrapper over Python's `socket.socket` constructor using `AF_INET` (IPv4) and `SOCK_STREAM` (TCP). 

I added `SO_REUSEADDR` at the socket configuration layer. This prevents the operating system from locking the network port in a `TIME_WAIT` state after a shutdown, allowing for instant re-binds. Data retrieval uses a controlled 1024-byte buffer allocation window to read raw network frames without overloading resources.

## Complexity Profile
* **Runtime Bounds:** $O(1)$ socket initialization, connection processing scales with incoming message length.
* **Space Constraints:** Fixed $O(\text{Buffer Size})$ memory limits per socket connection instance.