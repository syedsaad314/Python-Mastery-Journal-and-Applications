# Logic Breakdown: Saga State Machine Models
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Unlike two-phase commit architectures that rely on global resource locking, microservices need a way to manage transactions across separate services without holding open database connections indefinitely. To achieve this, we need a flexible data context that tracks the structural progress of a multi-step workflow.

## My Approach
I implemented a structured data token mapping (`SagaStatus`) alongside an immutable data container (`SagaContext`). This configuration explicitly monitors the system states as the transaction passes through different microservice steps, establishing a foundation for managing partial updates.

## Complexity Profile
* Runtime Bounds: Allocating and checking state configurations executes in $O(1)$ constant time.
* Space Constraints: Memory allocation stays tightly bounded at $O(1)$ for single transactions.