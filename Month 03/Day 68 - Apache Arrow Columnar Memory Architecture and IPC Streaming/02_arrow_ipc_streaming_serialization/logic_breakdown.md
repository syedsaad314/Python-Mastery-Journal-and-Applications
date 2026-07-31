# Logic Breakdown: Arrow IPC Binary Streaming
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Data transfers between microservices using JSON or CSV require heavy string parsing and float serialization CPU cycles at both producer and consumer ends.

## My Approach
I utilized PyArrow's `ipc.new_stream()` and `ipc.open_stream()`. The Arrow IPC format encapsulates FlatBuffers metadata alongside binary columnar data buffers, allowing receiver processes to read structured batches directly out of byte streams without string parsing or schema reconstruction passes.

## Complexity Profile
* Runtime Bounds: $O(N)$ memory transfer pass where $N$ is batch size in bytes.
* Space Constraints: $O(N)$ linear memory footprint for binary stream buffer.