# Architectural Specification: Async Saga Coordination Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## 1. High-Level Strategy
This engine replaces cross-node database blocks with eventual consistency models. Instead of forcing everyone to wait for a global transaction to commit, every step writes to its local database immediately. If something goes wrong later, the engine fires compensating tasks to clean up.

```plaintext
[Forward Track]: Order Placement ---> Inventory Hold ---> Payment Charge (Throws Exception ✗)
                                                                |
[Reverse Track]: Order Cancel    <--- Inventory Release <-------+ (Triggers Rollback 🔄)
```

## 2. Invariance Safety Matrix
* **Reverse Processing Policy**: The engine reads the history buffer backward to run compensations in reverse order. This ensures dependent resources are cleaned up in the correct sequence.
* **Fault Containment**: If a cleanup function itself throws an error, the engine catches it and continues down the stack, preventing a broken rollback from halting the entire cleanup process.

## 3. Algorithmic Complexity Profile
* Runtime Bounds: Running forward scales linearly at O(N) for N services. Reversing direction scales at O(K), where K matches the number of successfully finished steps.
* Space Constraints: Footprint tracks linearly at O(N) to keep tabs on the workflow steps and contexts.