# Logic Breakdown: Network Timeout Heuristics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
In a real-world network, nodes can experience slowdowns or drop offline entirely. If the coordinator waits indefinitely for a missing vote during the preparation phase, the entire system can stall, holding locks and blocking other operations.

## My Approach
I implemented an active timeout safety guard. During the voting collection step, the coordinator checks the incoming message pool against the expected participant list. If any node fails to respond within the window, the coordinator triggers a fail-safe abort to keep the system moving.

## Complexity Profile
* Runtime Bounds: Checking the list of expected participants runs in linear time $O(P)$.
* Space Constraints: Operates with an inline memory footprint of $O(1)$.