# Logic Breakdown: Asynchronous Circuit Breaker Pattern
**Engineer:** Syed Saad Bin Irfan

## The Problem
When a remote microservice drops, repeated automated retries can flood the failing target with traffic while stalling local async workers with long timeout delays.

## My Approach
I implemented an asynchronous circuit breaker state machine (`CLOSED`, `OPEN`, `HALF-OPEN`). 

The breaker wraps outbound network calls. If failures hit the configured threshold, the circuit trips to `OPEN` and rejects subsequent requests instantly, protecting local resources. Once the cooldown timer expires, the breaker enters `HALF-OPEN` to test the remote service with a single request, resetting automatically if it succeeds.

## Complexity Profile
* **Runtime Bounds:** Constant $O(1)$ state verification check and update overhead.
* **Space Constraints:** Constant $O(1)$ primitive state tracking fields.