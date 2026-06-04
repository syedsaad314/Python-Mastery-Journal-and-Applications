# Portfolio Code Review: Fault-Tolerant Distributed Process Supervisor Node
**Author:** Syed Saad Bin Irfan

## The Problem
In distributed architectures, child worker processes can crash due to memory bugs, unhandled exceptions, or network loss. If the master orchestrator doesn't monitor these failures, the system leaves orphaned resources and stalls execution pipelines.

## Engineering Standards Applied
* **Self-Healing Lifecycle Monitoring:** Uses a centralized control loop to actively poll the status of running child processes via `.is_alive()`. The loop catches non-zero exit codes immediately and triggers automatic recovery boots to keep workers online.
* **Defensive Failure Threshold Caps:** Features a reboot counter limit per node to handle recurring failures. If a worker gets trapped in a continuous crash loop, the supervisor quarantines the node to save system resources.
* **Isolated Process Error Isolation:** Wraps individual worker execution flows in completely separate operating system processes. This ensures that a fatal error or memory crash on one node won't disrupt or destabilize sibling processes in the cluster.