# Logic Breakdown: Immutable Causally Ordered Event Log
**Engineer:** Syed Saad Bin Irfan

## The Problem
Event-driven systems and microservices need to reconstruct state by replaying incoming event logs. If events are replayed in the order they happen to arrive over the network rather than their true causal order, the system can end up in an invalid state.

## My Approach
I engineered an **Append-Only Causally Sorted Event Stream**.

The log accepts incoming data frames regardless of their arrival order. Each frame carries its source vector clock metadata. Before replaying or auditing the stream, the engine runs a sorting pass that evaluates the causality metrics of each vector. This ensures that initialization events always sort before dependencies, providing a reliable sequence for state reconstruction.

## Complexity Profile
* **Runtime Bounds:** Appending is an $O(1)$ constant time operation. Sorting the log stream for consumption takes $O(T \log T \cdot N)$ time, where $T$ is the number of events and $N$ is the vector length.
* **Space Constraints:** Memory usage scales linearly at $O(T \cdot N)$ to retain the historical event trail.