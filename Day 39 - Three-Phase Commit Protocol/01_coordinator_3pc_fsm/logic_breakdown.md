# Logic Breakdown: 3PC Coordinator Finite State Machine
**Engineer:** Syed Saad Bin Irfan

## The Problem
Two-Phase Commit drops directly from a vote into a permanent global commitment, leaving no middle ground. If the system crashes at that boundary, external recovery tools cannot infer whether the coordinator decided to commit or abort before failing.

## My Approach
I implemented a strict **Three-Phase Coordinator Finite State Machine**.

This design introduces a crucial intermediate state: `PRE_COMMIT`. By separating the protocol into `CAN_COMMIT` (asking if updates are viable) and `PRE_COMMIT` (notifying that everyone voted yes, but before final execution), we guarantee that if any single node moves into the pre-commit state, every other node has already voted to commit. This explicit state progression provides the architectural predictability needed to handle coordinator failures without blocking.

## Complexity Profile
* **Runtime Bounds:** State validation checks and transition updates run in $O(1)$ constant time.
* **Space Constraints:** Requires $O(1)$ constant auxiliary memory space.