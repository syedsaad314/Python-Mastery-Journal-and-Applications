# Logic Breakdown: Query Projection Sync Channel
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Replaying thousands of historical events every time a user loads a dashboard ruins system performance. The write model needs to store raw history, but the read model needs immediate, flat answers.

## My Approach
I decoupled the read and write responsibilities using the CQRS pattern. As new events append to the write database, a projection worker updates a flat, read-optimized data view. This keeps reads fast and direct without touching the raw event history log.

## Complexity Profile
* Runtime Bounds: Processing updates and running read lookups both operate in constant O(1) time.
* Space Constraints: The read database uses O(A) space, where A represents the total number of distinct active aggregates.