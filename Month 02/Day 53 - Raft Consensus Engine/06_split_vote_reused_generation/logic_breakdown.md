# Logic Breakdown: Split Vote Term Advancement
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When a split-vote tie occurs, the cluster can become stuck if candidates wait around indefinitely in the same term. The system needs a clean way to reset and retry the election.

## My Approach
I built a ballot calculation filter. If a candidate's election window closes before it secures a clear majority, it declares a stalemate, increments the logical term counter, and kicks off a fresh election round.

## Complexity Profile
* Runtime Bounds: Conditional checking runs in constant $O(1)$ speeds.
* Space Constraints: Retains zero variable heap allocations matching an $O(1)$ space scale.