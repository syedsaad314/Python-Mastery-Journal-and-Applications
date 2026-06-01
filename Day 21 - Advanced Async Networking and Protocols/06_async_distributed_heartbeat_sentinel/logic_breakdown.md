# Logic Breakdown: Network Keep-Alive Heartbeat Sentinel
**Engineer:** Syed Saad Bin Irfan

## The Problem
Distributed nodes can crash or drop off the network silently without closing their TCP connections cleanly. We need an asynchronous parser to validate keep-alive heartbeats and detect silent drops.

## My Approach
I designed a validation class that extracts and checks incoming byte payloads against expected tokens. 

By tracking timestamps with the non-blocking `loop.time()` function, the sentinel evaluates incoming data frames efficiently, updating node status histories cleanly without adding lock contention or blocking the single-threaded async event loop.

## Complexity Profile
* **Runtime Bounds:** Packet verification runs in constant $O(1)$ string match lookups.
* **Space Constraints:** Constant $O(1)$ space required to store reference tokens and timestamp values.