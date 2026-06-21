# 📨 Enterprise Distributed Event Streaming Engine

┌───────────┐      Key Hashing      ┌─────────────────┐      Round-Robin      ┌────────────────┐
│  Producer │ ───────────────────►  │ Partitioned Log │ ────────────────────► │ Consumer Group │
└───────────┘      (O(1) Append)    │  [P0] [P1] [P2] │      (Auto-Balance)   │ [NodeA] [NodeB]│
└─────────────────┘                       └────────────────┘


[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](https://opensource.org/licenses/MIT)
[![Stability: Production](https://img.shields.io/badge/Architecture-Event__Driven-blueviolet?style=flat)](https://github.com/syedsaad314)

An enterprise-grade, high-throughput distributed event streaming log engine built from scratch in Python. The system provides an immutable append-only commit log with segmented topic partitioning, automatic consumer group balancing, granular offset checkpointing, and real-time processing telemetry dashboards.

---

## ⚡ Core Operational Features

* **Horizontal Log Partitioning:** Distributes topic data horizontally across independent, append-only logs via key hashing to enable maximum parallel processing speeds.
* **Dynamic Group Rebalancing:** Automatically balances partition ownership among active consumer group threads, optimizing resource use and handling node arrivals or departures.
* **Granular Offset Checkpoints:** Keeps message history completely immutable, tracking consumer progress via numerical offset markers to enable instant crash recovery.
* **Real-Time Telemetry Interface:** Features a live, responsive console panel built with `tabulate` and `colorama` to monitor consumer log lag and partition depths in real time.

---

## 📂 Modular Component Layout

The repository splits architectural concerns into clean, decoupled files:
* `message_broker.py` ── Coordinates horizontally scaled partition logs and tracks group offsets.
* `producer.py` ── Processes incoming data, handles partition routing keys, and manages sequencing.
* `consumer_group.py` ── Controls background polling thread worker lifecycles.
* `stream_dashboard.py` ── Component tracking and console UI rendering logic.
* `app_lifegiver.py` ── The main entry point that sets up configurations and initializes components.

---

## 📄 License

This repository is open-source software licensed under the terms of the [MIT License](LICENSE).

***

**Lead Engineer:** Syed Saad Bin Irfan  
*Undergraduate Software Engineering Student | Certified Prompt Engineer*