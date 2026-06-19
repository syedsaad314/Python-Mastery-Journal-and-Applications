# 📈 Enterprise Distributed Rate Limiter Engine

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat-flat&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-flat)](https://opensource.org/licenses/MIT)
[![Engine: Production](https://img.shields.io/badge/Architecture-Distributed__Mesh-orange?style=flat-flat)](https://github.com/syedsaad314)

An enterprise-grade, synchronized multi-node API traffic throttling and rate-limiting system built in Python. The engine simulates global API gateway nodes handling real-world traffic flows, using an optimized Token Bucket algorithm and asynchronous synchronization loops to protect downstream services from distributed traffic surges.

---

## ⚡ Core Operational Features

* **Mathematical Token Refills:** Evaluates request compliance instantly by calculating token replenishment mathematically on the fly, eliminating the need for expensive background refill threads.
* **Asynchronous Cluster Synchronization:** Balances local execution speeds with cluster-wide security by periodically reconciling node usage metrics into a unified, shared traffic baseline.
* **Thread-Safe Memory Management:** Uses explicit, fine-grained thread locking structures (`threading.Lock`) within each node to safely handle concurrent traffic packets without risking data corruption.
* **Live Telemetry Interface:** Features an interactive terminal dashboard built with `tabulate` and `colorama` that displays request tracking metrics, individual node balances, and traffic spike warnings in real time.

---

## 📂 Modular Component Layout

The repository splits architectural concerns into clean, decoupled files:
* `rate_bucket.py` ── Core Token Bucket calculation logic and resource allocation.
* `cluster_sync.py` ── Synchronization loops that reconcile token balances across active nodes.
* `traffic_generator.py` ── Synthetic traffic generation simulating standard operations vs sudden surges.
* `monitor_dashboard.py` ── Layout, formatting, and terminal UI rendering for the telemetry system.
* `app_lifegiver.py` ── The main orchestration script that configures nodes and runs the application.

---

## 📄 License

This repository is open-source software licensed under the terms of the [MIT License](LICENSE).

***

**Lead Engineer:** Syed Saad Bin Irfan  
*Undergraduate Software Engineering Student | Certified Prompt Engineer*