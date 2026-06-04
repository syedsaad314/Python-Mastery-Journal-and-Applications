# Logic Breakdown: Duplex Communication Channels via Binary Framing
**Engineer:** Syed Saad Bin Irfan

## The Problem
Using shared objects across processes can cause contention issues. When two processes need to sync via distinct request-response sequences, multi-producer queues add unnecessary synchronization overhead.

## My Approach
I utilized a low-overhead, hardware-backed bidirectional `multiprocessing.Pipe(duplex=True)`. 

Instead of passing heavy arbitrary dictionaries down the stream, I implemented a micro-protocol string framer format (`ACTION::PAYLOAD`). This design ensures that the data stays tiny and easy to parse, isolating process states and creating a clear architectural boundary between components.

## Complexity Profile
* **Runtime Bounds:** Sequential write-read sequences run in a clean $O(1)$ timeframe.
* **Space Constraints:** Variable memory footprint proportional to the length of the command string transmitted.