# Logic Breakdown: Raft Term Epoch Tracking
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
In partitioned networks, an isolated leader might continue processing requests without knowing a new leader has been elected elsewhere, creating conflicting, out-of-date terms.

## My Approach
I implemented a **Term Epoch Validation Engine**.
Raft breaks time down into numerical epochs called terms. Every message carries the sender's current term number. If a node receives a message with an older term number, it rejects it instantly. If a leader sees a message with a newer term number, it immediately steps down to a follower role and updates its term counter, ensuring obsolete nodes cannot corrupt data.

## Complexity Profile
* **Runtime Bounds:** Integer term validations complete instantly in $O(1)$ constant time.
* **Space Constraints:** Uses a fixed $O(1)$ constant tracking footprint.