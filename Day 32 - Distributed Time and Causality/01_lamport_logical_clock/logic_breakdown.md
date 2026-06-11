# Logic Breakdown: Lamport Logical Clock
**Engineer:** Syed Saad Bin Irfan

## The Problem
In distributed systems, physical timestamps cannot reliably prove whether event $A$ happened before event $B$ due to hardware clock drift across different machines.

## My Approach
I implemented **Lamport's Scalar Logical Clock Algorithm**. 

Instead of tracking real-world minutes or seconds, the clock uses a simple monotonic integer counter. Every local operation increments this counter by 1. When a node sends a message, it includes its current clock value. When another node receives that message, it updates its local counter to be greater than both its current value and the incoming timestamp ($\max(\text{local}, \text{incoming}) + 1$). This guarantees that the sender's event always logically precedes the receiver's event.

## Complexity Profile
* **Runtime Bounds:** Every clock update executes in $O(1)$ constant time.
* **Space Constraints:** Requires $O(1)$ auxiliary space per node to maintain a single integer counter.