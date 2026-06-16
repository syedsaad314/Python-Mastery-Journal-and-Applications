# Portfolio Code Review: Peer-to-Peer Cooperative Transaction Recovery Simulator
**Author:** Syed Saad Bin Irfan

## Practical Context
This simulator models how distributed nodes resolve pending states when a central manager vanishes, demonstrating how systems use peer-to-peer coordination to keep data consistent without blocking operations.

## Engineering Standards Applied
* **Decentralized State Evaluation:** Collects and analyzes internal states directly from surviving nodes, bypassing the need for a central coordinator during recovery.
* **Deterministic 3PC Resolution Rules:** Applies strict consensus invariants to pooled states, ensuring the cluster resolves transactions reliably and accurately.
* **Non-Blocking Execution Guards:** Uses state-based recovery logic to let nodes resolve transactions and release resource locks safely, preventing data freezes under standard coordinator failures.