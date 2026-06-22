# Logic Breakdown: Consumer Offset Commit Tracking
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a consumer process crashes mid-execution, the system needs a way to know exactly where that consumer left off so it can resume processing without skipping data or re-reading the entire log history.

## My Approach
I engineered an **Asynchronous Consumer Offset Commit Tracker**.

Instead of deleting messages from the log once they are read, the log remains immutable and persistent. The tracker logs a sequential counter, known as an offset, for each consumer group. When a consumer restarts, it queries the offset tracker for its last committed checkpoint and safely resumes reading from that exact coordinate in the log.

## Complexity Profile
* **Runtime Bounds:** Registering and looking up offsets takes $O(1)$ constant time.
* **Space Constraints:** Tracks state at $O(K)$ space relative to active partition keys $K$.