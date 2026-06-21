# 📊 Distributed Financial Ledger System

┌─────────────────────────┐
│ Transaction Coordinator │
└─────────────────────────┘
│               │
│ (1) Prepare   │ (1) Prepare
▼               ▼
┌──────────┐    ┌──────────┐
│  Node A  │    │  Node B  │  ◄─── Write-Ahead Logging (WAL)
└──────────┘    └──────────┘


[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://opensource.org/licenses/MIT)
[![Stability: Stable](https://img.shields.io/badge/Architecture-Distributed__Transactions-blue?style=flat)](https://github.com/syedsaad314)

An enterprise-grade distributed banking ledger transaction system built from scratch in Python. The system provides atomic financial updates across decoupled database nodes using the Two-Phase Commit protocol, supported by write-ahead logging (WAL) safety checkpoints and real-time ledger metric auditing.

---

## ⚡ Core Operational Features

* **Two-Phase Commit Integration:** Guarantees strict transactional atomic consistency by splitting writes into clear verification and commitment phases.
* **Write-Ahead Logging Protection:** Logs transaction milestones to persistent storage before updating runtime values, enabling reliable state recovery after system crashes.
* **Atomic Rollback Controls:** Automatically intercepts balance rejections or network issues, rolling back active transactions across all nodes to prevent data mismatches.
* **Clean Metrics Presentation:** Uses a scannable console dashboard built with `tabulate` to display balance updates and node verification status in real time.

---

## 📂 Modular Component Layout

The repository splits architectural concerns into clean, decoupled files:
* `transaction.py` ── Defines core transaction structures tracking safe multi-node financial updates.
* `ledger.py` ── Manages account balances, write-ahead logs, and uncommitted transaction staging fields.
* `participant.py` ── Connects coordinator commands to local account spaces and processes commit steps.
* `coordinator.py` ── Directs 2PC execution flows across all participant nodes in the cluster.
* `metrics.py` ── Formats and displays account balance tables and transaction metrics to the console.
* `main.py` ── Sets up participant databases, initializes coordinators, and runs transaction profiles.

---

## 📄 License

This repository is open-source software licensed under the terms of the [MIT License](LICENSE).

***

**Lead Engineer:** Syed Saad Bin Irfan  
*Undergraduate Software Engineering Student | Certified Prompt Engineer*