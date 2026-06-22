# 📊 Replicated Key-Value Store System

   ┌────────────────────────┐
   │ node_host_01 (LEADER)  │ ◄─── Term Epoch Tracking
   └────────────────────────┘
     │                    │
     │ (RPC Append)       │ (RPC Append)
     ▼                    ▼
┌──────────────┐     ┌──────────────┐
│ node_host_02 │     │ node_host_03 │ ◄─── Quorum Log Verification
└──────────────┘     └──────────────┘


[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://opensource.org/licenses/MIT)
[![Stability: Production](https://img.shields.io/badge/Consensus-Raft-blueviolet?style=flat)](https://github.com/syedsaad314)

A production-ready distributed fault-tolerant replicated storage system built from scratch in Python. The architecture provides consistent key-value state management across decoupled cluster nodes using Raft consensus principles, supported by write-ahead logging (WAL) and strict majority quorum validation models.

---

## ⚡ Core Operational Features

* **Raft Election Workflows:** Implements term transitions and voting rules to handle node timeouts and elect a single leader safely.
* **Quorum-Backed Log Replication:** Processes client commands via the leader node and replicates them to followers, committing writes only after majority confirmation.
* **Log Progress Protections:** Followers review a candidate's log term and length before voting, ensuring leaders always contain all committed cluster history.
* **Tabular Cluster Metrics:** Includes a scannable terminal dashboard built with `tabulate` to track consensus roles, term epochs, and state machine updates in real time.

---

## 📂 Modular Component Layout

The repository splits architectural concerns into clean, decoupled files:
* `state.py` ── Encapsulates node consensus status, terms, roles, and voted-for metrics.
* `storage.py` ── Manages write-ahead logs and the active key-value state machine storage engine.
* `node.py` ── Handles RequestVote checks and processes replicated log appends from the leader.
* `cluster.py` ── Models RPC network delivery to simulate cluster voting and log replication.
* `metrics.py` ── Formats and displays cluster status, term counts, and data logs using clean tables.
* `main.py` ── Sets up a multi-node cluster, triggers leader elections, and processes consensus data writes.

---

## 📄 License

This repository is open-source software licensed under the terms of the [MIT License](LICENSE).

***

**Lead Engineer:** Syed Saad Bin Irfan  
*Undergraduate Software Engineering Student | Certified Prompt Engineer*