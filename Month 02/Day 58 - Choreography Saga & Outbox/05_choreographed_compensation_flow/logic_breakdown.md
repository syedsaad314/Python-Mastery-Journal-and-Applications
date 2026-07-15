# Logic Breakdown: Choreographed Compensation Flows
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Without a central orchestrator tracking the execution state, a failure down the line (like a rejected credit card payment) can leave previous services hanging out of sync unless they are actively listening for bad news.

## My Approach
I built decentralized error handling directly into the microservice domain models. Each service listens to the global event channel for failure notifications relevant to its domain. When a failure signal matches its open transaction tracking key, the service automatically runs its local compensation routine.

## Complexity Profile
* Runtime Bounds: Matching and executing compensations runs in O(1) time using hashed context updates.
* Space Constraints: Tracking execution flags requires a constant O(1) footprint per transaction entry.