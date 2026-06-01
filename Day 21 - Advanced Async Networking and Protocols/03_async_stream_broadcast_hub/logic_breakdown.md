# Logic Breakdown: Asynchronous Publisher-Subscriber Streaming Hub
**Engineer:** Syed Saad Bin Irfan

## The Problem
When running real-time services like chat systems or telemetry feeds, a single broadcast message can stall the system if one slow client socket delays the entire distribution pipeline.

## My Approach
I created a centralized state class that aggregates active `asyncio.StreamWriter` connections within a Python `set`. 

The hub loops through active client connections to dispatch data packets. If a connection fails due to a `BrokenPipeError` or client disconnect, the system catches the error defensively and purges the dead socket from the registry, keeping the broadcast loop efficient and stable.

## Complexity Profile
* **Runtime Bounds:** Broadcast runs in linear $O(N)$ time, where $N$ is the number of active subscribers.
* **Space Constraints:** Scales at $O(N)$ memory allocations to maintain active subscriber stream references.