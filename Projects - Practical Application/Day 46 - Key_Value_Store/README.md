# Log-Reconciled Key-Value Store System

An enterprise-grade fault-tolerant distributed key-value store built from scratch in Python, optimized for Month 02 architecture tracking layout. The platform implements dynamic log reconciliation protocols to identify log divergence points, truncate conflicting entries, and align node state machines across network clusters safely.

## Core Operational Features

* Reverse Backtracking Identification: Scans backward through logs during network syncs to find the last valid consensus match point between leaders and followers.
* Automated Log Truncation: Automatically identifies term mismatches and safely trims conflicting uncommitted log entries to clean follower storage.
* State Machine Consistency Alignment: Limits database updates strictly to the leader's validated commit_index boundary, ensuring uncommitted records never alter active memory.
* Decoupled Telemetry Console: Uses a terminal dashboard built with tabulate to track cluster roles, terms, commit statuses, and log history layouts in real time.

## Modular Component Layout

The repository splits architectural concerns into clean, decoupled files:
* models.py: Defines individual log entries that carry term numbers and state change commands.
* storage.py: Manages a node's local log sequence and applies committed records to memory.
* consensus.py: Coordinates pointer backtracking, conflict tracking, and log truncation.
* node.py: Tracks term counters, commit boundaries, and cluster node configurations.
* network.py: Intercepts out-of-sync followers and triggers the log reconciliation engine.
* main.py: Simulates out-of-sync cluster states and runs log reconciliation routines.

## License

This repository is open-source software licensed under the terms of the MIT License.

***

**Lead Engineer:** Syed Saad Bin Irfan
*Undergraduate Software Engineering Student | Certified Prompt Engineer*