# Portfolio Code Review: Raft Leader Election Core Engine
**Author:** Syed Saad Bin Irfan

## Practical Context
This engine implements the core leader election and state management behaviors that power highly reliable, fault-tolerant cloud infrastructures, ensuring that a cluster can automatically recover and elect a new leader if the active one fails.

## Engineering Standards Applied
* **Strict Term Guard Rails:** Follows Raft safety rules by ignoring vote requests or heartbeats from older terms, preventing out-of-date nodes from disrupting the cluster.
* **Randomized Timeout Adjustments:** Generates unique timeouts dynamically for each node, splitting up timers to prevent split-vote deadlocks and speed up elections.
* **Instant Demotion Tracking:** Forces leaders or candidates to immediately step down and update their state if they discover a higher term counter, quickly resolving split-brain anomalies.