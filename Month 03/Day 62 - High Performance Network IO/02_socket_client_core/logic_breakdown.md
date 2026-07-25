# Logic Breakdown: Non-Blocking Client Engine
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Network latency spikes during outbound connections can hang synchronous client calls for up to 75 seconds while waiting for TCP response retries.

## My Approach
I set the client to non-blocking and caught `EINPROGRESS` status flags directly from the operating system network stack. This prevents the application from locking up, allowing it to handle other tasks while the hardware finishes the three-way TCP handshake.

## Complexity Profile
* Runtime Bounds: Connection requests resolve in O(1) operational complexity.
* Space Constraints: O(1) absolute constant execution memory footprint.