# Logic Breakdown: Write-Ahead Logging (WAL) for Transactions
**Engineer:** Syed Saad Bin Irfan

## The Problem
If a node crashes mid-transaction, its volatile RAM memory is completely wiped. Without a persistent history of its state before the crash, the node cannot figure out what happened when it reboots, risking inconsistencies.

## My Approach
I built a structured **Write-Ahead Log (WAL)** engine interface.

Before sending any network request or changing its in-memory state, the system appends the intended state change to an immutable log file on disk. This ensure that even if power cuts out instantly, the node can read this log on startup to safely reconstruct its state and complete the transaction.

## Complexity Profile
* **Runtime Bounds:** Appending a log record runs in $O(1)$ constant time.
* **Space Constraints:** Memory and disk usage scale linearly at $O(L)$ with the number of log events $L$.