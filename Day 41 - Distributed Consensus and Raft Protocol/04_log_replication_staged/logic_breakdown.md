# Logic Breakdown: Staged Log Replication Entry
**Engineer:** Syed Saad Bin Irfan

## The Problem
A leader cannot immediately execute commands sent by a client. If the leader crashes before other nodes receive the update, the systems will drift out of sync.

## My Approach
I designed a **Staged Local Ledger Appender**.

Commands are stored as tentative log entries rather than being applied directly to the database state machine. This keeps entries isolated: they are written locally and sent to peers, but remain uncommitted until majority verification is complete.

## Complexity Profile
* **Runtime Bounds:** Appending an entry to the log array runs in $O(1)$ amortized constant time.
* **Space Constraints:** Memory scales linearly at $O(L)$ relative to the log length $L$.