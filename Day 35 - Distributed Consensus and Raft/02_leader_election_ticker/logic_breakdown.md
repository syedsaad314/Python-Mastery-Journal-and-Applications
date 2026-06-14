# Logic Breakdown: Randomized Election Timeout Ticker
**Engineer:** Syed Saad Bin Irfan

## The Problem
If all cluster nodes use the exact same timeout duration, they will all detect a leader's failure and transition to candidates at the exact same moment. This leads to a permanent **split-vote deadlock** where every node votes for itself, preventing anyone from reaching a majority.

## My Approach
I engineered a **Randomized Election Timeout Ticker** that assigns each node a unique timeout within a specific window (typically 150ms to 300ms).

This time variance breaks the symmetry of the cluster. The node with the shortest timeout will wake up first, transition to a candidate, increment its term, and collect votes from the other followers before their timeouts can expire, ensuring clean leader election.

## Complexity Profile
* **Runtime Bounds:** Generating the randomized duration executes in $O(1)$ time.
* **Space Constraints:** Uses $O(1)$ constant space.