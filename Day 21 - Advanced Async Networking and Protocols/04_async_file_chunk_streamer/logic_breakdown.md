# Logic Breakdown: Non-Blocking File Chunk Streaming
**Engineer:** Syed Saad Bin Irfan

## The Problem
Standard Python file methods are synchronous and blocking. Reading a massive data file directly inside an async function freezes the event loop, stalling network traffic and socket response lines.

## My Approach
I combined async generators with `loop.run_in_executor()`. 

The class tracks data offsets and streams file chunks from a background `ThreadPoolExecutor`. By wrapping disk access in an `async for` loop generator, the application streams large files smoothly while keeping the primary event loop completely responsive for network connections.

## Complexity Profile
* **Runtime Bounds:** Memory reads process in linear $O(F / B)$ execution waves, where $F$ is file size and $B$ is chunk size.
* **Space Constraints:** Bounded to a flat $O(B)$ memory buffer footprint per chunk, preventing memory usage spikes.