# Distributed Two-Phase Commit (2PC) Transaction Engine

## Core Architectural Guarantees
* **Distributed Atomicity Guarantee**: Guarantees that multi-node operations either complete successfully across all participants or roll back completely, ensuring data consistency.
* **Isolated Prepare Workspaces**: Protects production data by holding modifications in temporary isolation caches until the coordinator verifies unanimous cluster agreement.
* **Timeout Resiliency**: Prevents resource locking deadlocks by automatically aborting transactions if a node drops offline or fails to vote within the network window.

## Component Layout
* `models.py`: Holds protocol data contracts and command enumeration tokens.
* `network_stub.py`: Connects components and simulates network partitions or timeouts.
* `participant_node.py`: Manages individual shard storage, isolation caches, and write-ahead logs.
* `coordinator.py`: Orchestrates the voting and execution phases across the cluster.