# Logic Breakdown: Sliding Window API Rate Limiter
**Engineer:** Syed Saad Bin Irfan

## The Problem
Basic fixed-window rate limiters are vulnerable to traffic bursts at window edges. For instance, if an API allows 100 requests per hour, a user could send all 100 requests at 11:59 and another 100 at 12:01. This creates a dangerous spike that doubles the expected traffic load, exposing downstream servers to denial-of-service failures.

## My Approach
I built a real-time sliding window engine using a dictionary that maps user identifiers to dynamic timestamp arrays. Every time an API call drops in, the system calculates a strict time window backwards from the current moment. It discards any entries older than this cutoff and checks the remaining log count against the system limit.

## Critical Thinking
*   **Time Complexity:** Pruning oldest elements scales relative to the volume of requests per individual burst window, averaging $O(K)$.
*   **Space Complexity:** Consumes $O(U \times K)$ RAM, tracking active user sessions ($U$) and their request frequencies within the rolling timeframe ($K$).

This approach eliminates the edge-burst vulnerability of fixed windows, making it ideal for securing internal payment gateways and prediction service endpoints.