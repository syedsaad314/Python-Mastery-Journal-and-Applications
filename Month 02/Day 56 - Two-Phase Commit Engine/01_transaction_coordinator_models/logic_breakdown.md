# Logic Breakdown: Transaction Coordinator State Models
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Distributed atomicity requires a centralized state engine to act as a single source of truth for multi-node transactions. Without clear status state tracking, a coordinator cannot safely resume or roll back operations if it crashes mid-transaction.

## My Approach
I implemented an explicit status enumeration mapping (`CoordinatorState`) to represent the phase transitions of the protocol. Wrapping these inside an immutable data container provides a structured foundation for building multi-step validation checks.

## Complexity Profile
* Runtime Bounds: Accessing and updating individual state records evaluates in $O(1)$ time.
* Space Constraints: Allocates memory linearly ($O(P)$) based on the number of tracked participant IDs.