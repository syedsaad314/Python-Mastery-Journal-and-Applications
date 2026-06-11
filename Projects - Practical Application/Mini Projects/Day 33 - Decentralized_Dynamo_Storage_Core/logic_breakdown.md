# Portfolio Code Review: Decentralized Dynamo Storage Core
**Author:** Syed Saad Bin Irfan

## Practical Context
This engine implements the masterless write routing, quorum checking, and read repair behaviors that power high-availability, zero-downtime distributed databases like Amazon's DynamoDB or Apache Cassandra.

## Engineering Standards Applied
* **Configurable Strict Quorum Paths:** Allows applications to balance consistency and speed by adjusting read and write quorum parameters dynamically based on workload needs.
* **Inline Read Repair Guard rails:** Fixes out-of-sync nodes on the fly during read operations, reducing the reliance on heavy background repair jobs.
* **Masterless Write Isolation:** Routes writes across the cluster without a single point of failure, maximizing data availability and scale-out performance.