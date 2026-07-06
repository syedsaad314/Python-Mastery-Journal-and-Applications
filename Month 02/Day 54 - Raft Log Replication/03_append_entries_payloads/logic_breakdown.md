# Logic Breakdown: AppendEntries Replication Payloads
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Leaders must tailor replication payloads for each peer. The message needs to slice the log from the correct point based on what that specific peer has already received, while including the context needed for validation.

## My Approach
I implemented a sliding slicing routine based on a peer tracking index. The function looks up the preceding history entry to compute the validation terms, and packs all newer unreplcated items into a single outbound network payload.

## Complexity Profile
* Runtime Bounds: Slicing the log runs in $O(M)$ time, where $M$ is the number of catch-up entries being sent.
* Space Constraints: Creating the slice uses $O(M)$ auxiliary memory variables.