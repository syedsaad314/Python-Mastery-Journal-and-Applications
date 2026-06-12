# Logic Breakdown: Idempotent Transaction Execution Log
**Engineer:** Syed Saad Bin Irfan

## The Problem
In distributed networks, messages can be duplicated or re-sent due to network timeouts. If a client sends a transaction request, experiences a timeout, and retries the request, the system risks processing the transaction twice, which can lead to issues like double-charging a user.

## My Approach
I engineered an **Idempotent Ingest Gateway Filter**.

The gateway tracks unique identifiers attached to each incoming transaction request. If a request arrives with an identifier that is already in the log, the gateway drops it as a duplicate and returns the previous result. This deduplication layer guarantees that transactions are executed exactly once, even when clients retry requests over unstable networks.

## Complexity Profile
* **Runtime Bounds:** Identifiers are verified and logged in $O(1)$ constant time using a hash set.
* **Space Constraints:** Memory usage scales linearly at $O(K)$ relative to the total number of unique transaction keys $K$ tracked by the gateway.