# Portfolio Code Review: Distributed Causal Chat Messaging Engine
**Author:** Syed Saad Bin Irfan

## Practical Context
This engine simulates decentralized messaging behavior (similar to the underlying core protocols used in matrix communication networks or distributed chat platforms). It ensures conversational coherence across clients without relying on a centralized database coordinator.

## Engineering Standards Applied
* **Conversational Consistency Guarantee:** Employs explicit vector checks to block answers from displaying before their corresponding questions, preventing out-of-order text rendering.
* **Decentralized Structural Coordination:** Each client tracks and verifies message dependencies independently using its own vector state clock, removing the risk of a single point of failure.
* **Resilient Holdback Queues:** Isolates unstable message reception logic from the UI layer by buffering out-of-order frames and releasing them automatically once all causal conditions are met.