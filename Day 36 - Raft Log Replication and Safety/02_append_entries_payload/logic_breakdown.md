# Logic Breakdown: AppendEntries RPC Data Structural Layout
**Engineer:** Syed Saad Bin Irfan

## The Problem
A leader cannot simply send new log entries to followers blindly. Followers need context to verify their local logs match the leader's log exactly up to that point. Without this validation, gaps or conflicting histories can go unnoticed, breaking consensus guarantees.

## My Approach
I implemented an **AppendEntries RPC Payload Frame Builder**.

The schema includes the leader's metadata along with two critical fields: `prev_log_index` and `prev_log_term`. These parameters allow followers to perform an inductive consistency check, ensuring their log history matches the leader's exactly before appending the new entries.

## Complexity Profile
* **Runtime Bounds:** Building the RPC dictionary packet completes in $O(1)$ constant time.
* **Space Constraints:** Storage scales at $O(M)$ where $M$ is the size of the entries payload being sent.