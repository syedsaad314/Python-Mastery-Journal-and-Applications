# Logic Breakdown: AppendEntries Log Replication Mechanism
**Engineer:** Syed Saad Bin Irfan

## The Problem
If a leader crashes mid-transaction or network partitions form, follower logs can fall out of sync or conflict with the leader's history. The system must guarantee that all nodes eventually converge on an identical, ordered history of commands.

## My Approach
I engineered an entry verification pipeline using Raft's **AppendEntries Log Matching Invariant**.

When the leader sends log updates, it includes the index and term of the *preceding* record (`prev_log_index`, `prev_log_term`). The follower verifies this entry against its local log. If a mismatch is detected, the follower rejects the write, forcing the leader to back up and locate the exact point where their histories diverged. Once a match is confirmed, any conflicting historical records are truncated, ensuring logs converge reliably across nodes.

## Complexity Profile
* **Runtime Bounds:** Log checks run in $O(1)$ constant time, while log updates scale linearly ($O(E)$) based on the number of entries being appended.
* **Space Constraints:** Memory usage grows linearly ($O(L)$) relative to the total number of entries stored in the log.