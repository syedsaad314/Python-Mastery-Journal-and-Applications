# Logic Breakdown: Client Session Idempotency Tracking
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a leader receives a client write request, commits it to the state machine, but crashes before sending the success response, the client will retry the write. Without deduplication, the system would execute the mutation twice, corrupting the data state.

## My Approach
I built a dual-key session tracking hash store mapping `client_id` and unique `sequence_id` fields. If a retried request comes in with a matching sequence ID, the engine skips execution entirely and returns the cached response from the previous transaction, ensuring linearizable mutations.

## Complexity Profile
* Runtime Bounds: Hash table lookups resolve in constant amortized time bounds of $O(1)$.
* Space Constraints: Scales at $O(C \times S)$ matching active client tracking sizes $C$ and session depth lengths $S$.