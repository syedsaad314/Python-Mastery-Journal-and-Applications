# Engineering Log Overview: Distributed Raft Consensus Engine
**Lead Engineer:** Syed Saad Bin Irfan

## 1. The Core Problem
To build a strongly consistent distributed system, a cluster must agree on a single, linear sequence of operations. Without a coordinator, nodes risk executing conflicting operations. However, a static coordinator creates a single point of failure. We need a resilient way to dynamically elect a single, trusted leader to manage the cluster state safely.

## 2. Architectural Brainstorming & Trade-offs
We chose the Raft Consensus model due to its clear separation of concerns, dividing consensus into distinct phases: Leader Election, Log Replication, and Safety.

### Balancing Timeouts and Term Invariants
* **The Balancing Act:** If heartbeats are sent too slowly, followers will assume the leader has failed and trigger constant, disruptive elections. If heartbeats are sent too quickly, they saturate network bandwidth.
* **The Safety Matrix:** We set up a two-step defense. First, randomized election timeouts shake up node campaigns to prevent split-vote deadlocks. Second, we treat logical terms as a strict global clock, forcing outdated nodes to step down instantly if they encounter a higher term counter.

## 3. Engineering Implementation Details
* **Ballot Majorities:** Elections require an absolute majority: $\lfloor N/2 \rfloor + 1$. This mathematical rule guarantees that only one leader can be elected during a given term, preventing split-brain scenarios.
* **RPC Messaging Stubs:** We built an event-driven network layout that handles vote solicitation and leader heartbeats synchronously without adding multi-threading complexity to this phase.