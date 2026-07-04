# Logic Breakdown: RequestVote RPC Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
To guarantee safety, a cluster must never allow two different nodes to become leader during the same term. Nodes must safely track their voting history to prevent double-voting.

## My Approach
I built a transaction gate inside the ballot evaluation logic. A node records its vote in a persistent state variable (`voted_for`) for the current term. Any other vote request within that same term is instantly rejected.

## Complexity Profile
* Runtime Bounds: Condition evaluations execute in $O(1)$ constant steps.
* Space Constraints: Uses $O(1)$ memory variables to track state.