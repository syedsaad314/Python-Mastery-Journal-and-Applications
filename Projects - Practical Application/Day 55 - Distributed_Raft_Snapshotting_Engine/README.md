# Distributed Raft Snapshotting & Compaction Engine

## Core Guarantees & Operational Principles
* **Safe Log Compaction**: Guarantees that only fully committed entries are removed from memory, protecting data integrity.
* **Fast-Forward Follower Catch-Up**: Automatically detects severely lagging nodes and uses `InstallSnapshot` payloads to catch them up instantly, bypassing tedious entry-by-entry replays.
* **Accurate Coordinate Offsets**: Uses tracking variables (`last_included_index`) to maintain accurate log indexing even after older entries are purged from the array.

## Layout Breakdown
* `models.py`: Defines structural payloads for both standard updates and snapshot messages.
* `state_machine.py`: Drives database updates and manages snapshot captures and restores.
* `raft_node.py`: Implements log trimming, pointer management, and snapshot installation rules.