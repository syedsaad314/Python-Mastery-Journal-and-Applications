# Engineering Log Overview: Log Compaction & Snapshot Drivers
**Lead Engineer:** Syed Saad Bin Irfan

## 1. The Core Problem
As a distributed consensus cluster processes client traffic, its log grows indefinitely. This creates two distinct problems: it risks running out of disk and memory space, and it makes node recovery incredibly slow, as a restarting node must replay millions of historical entries to rebuild its state.

## 2. Architectural Design Choices
We resolved this by implementing state snapshotting alongside our logging engine.

```plaintext
Client Writes -> Log Appends -> Threshold Exceeded -> State Snapshot -> Log Discarded & Memory Reclaimed