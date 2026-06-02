# Logic Breakdown: Weak References and Garbage Collection
**Engineer:** Syed Saad Bin Irfan

## The Problem
Circular references (where object A points to object B, and object B points back to object A) artificially inflate internal reference counters, blocking the garbage collector and causing persistent memory leaks.

## My Approach
I leveraged Python's `weakref` module to break reference cycles. 

Standard assignments create strong reference links, which increments an object's internal tracking counter. A weak reference provides access to an object without incrementing its counter. As soon as the last strong reference is severed, the object is immediately garbage collected and its memory is reclaimed, completely eliminating cache retention leaks.

## Complexity Profile
* **Runtime Bounds:** Lookups resolve instantly in $O(1)$ constant time.
* **Space Constraints:** Zero memory structural overhead ($O(1)$ storage spaces).