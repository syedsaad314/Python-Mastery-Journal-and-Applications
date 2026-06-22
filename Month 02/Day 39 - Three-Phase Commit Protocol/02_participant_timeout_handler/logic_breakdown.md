# Logic Breakdown: 3PC Participant State-Aware Timeout Fallbacks
**Engineer:** Syed Saad Bin Irfan

## The Problem
In 2PC, if a prepared participant loses contact with the coordinator, it has no way of knowing how other nodes voted, forcing it to hold locks and block indefinitely to prevent data corruption.

## My Approach
I built a **State-Aware Timeout Resolution Engine** for 3PC participants.

This script implements two structural rules:
1. If a node times out while in `INIT` or `CAN_COMMIT_RECEIVED`, it safely defaults to an abort since the transaction hasn't progressed to consensus.
2. If a node times out while in `PRE_COMMIT_RECEIVED`, it can safely transition to a commit on its own. Because it reached this phase, it knows every other peer already voted yes during the `CAN_COMMIT` stage, ensuring the transaction can complete safely without blocking.

## Complexity Profile
* **Runtime Bounds:** Evaluates conditions and updates states in $O(1)$ constant time.
* **Space Constraints:** Operates within $O(1)$ constant tracking space.