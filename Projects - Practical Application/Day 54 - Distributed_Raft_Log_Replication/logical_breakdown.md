# Engineering Log Overview: Log Replication & State Machine Drivers
**Lead Engineer:** Syed Saad Bin Irfan

## 1. The Core Problem
Electing a leader is only half the battle. To maintain absolute linearizability across a distributed cluster, every node must execute the exact same commands in the exact same sequence. We need a way to distribute client updates, verify historical alignment, and execute commands only when they are safely committed.

## 2. Architectural Brainstorming & Convergence
We addressed this by turning the `AppendEntries` payload into an active replication engine.

```plaintext
Client Write -> Leader Log -> Network Broadcast -> Follower Alignment Checks -> Majority Verification -> State Machine Execution