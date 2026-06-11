# Logic Breakdown: Causal Delivery Network Middleware Simulation
**Engineer:** Syed Saad Bin Irfan

## The Problem
In decentralized environments, network channels are unpredictable. If a user posts an answer to a question, network jitter can cause the answer to land at some nodes before the question itself arrives, confusing the application state.

## My Approach
I built a **Holdback Buffer Middleware Architecture** that enforces causal order.

When a message arrives, the middleware inspects its attached vector clock. It verifies that the sender is exactly one step ahead of the last message received from them, and that the message doesn't require updates from other servers that this node hasn't seen yet. If these conditions aren't met, the message is safely held in a buffer and released only when the missing context arrives.

## Complexity Profile
* **Runtime Bounds:** Processing a packet takes $O(B \cdot N)$ worst-case time, where $B$ is the number of messages currently held in the buffer and $N$ is the number of nodes tracked in the system.
* **Space Constraints:** Memory usage scales at $O(B \cdot N)$ to store the buffered messages along with their tracking vectors.