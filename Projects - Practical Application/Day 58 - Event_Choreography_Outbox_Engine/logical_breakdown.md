# Architectural Specification: Choreography Saga Flow Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## 1. Decentralized Execution Strategy
Unlike centralized orchestration, the Choreography pattern distributes workflow control across all participating services. Each microservice works independently—listening for events from other domains, performing its internal logic, and emitting new events to trigger downstream actions.

```plaintext
[SUCCESS WORKFLOW]
OrderService (Outbox Commit) ──[ORDER_SUBMITTED]──> InventoryService (Hold Stock)
                                                            │
                                                     [STOCK_ALLOCATED]
                                                            ▼
                                                     BillingService (Charge Card ✓)

[COMPENSATION ROLLBACK WORKFLOW]
BillingService (Charge Fails ❌) ──[BILLING_FAILED]──> OrderService (Mark Cancelled 🔄)
                                                └──> InventoryService (Release Stock 🔄)
```

## 2. Structural Guarantees
* **Dual-Write Resolution**: Using the Transactional Outbox pattern guarantees that a service won't send an event if its local database update fails. If the local commit works, the event is safely staged in the outbox to be delivered later.
* **Idempotency Protection**: To prevent errors from duplicate event redeliveries, every service checks incoming message IDs against an internal deduplication cache before executing any business updates.

## 3. Algorithmic Complexity Profile
* Runtime Bounds: Event routing and deduplication checks run in constant O(1) time. The asynchronous execution chain scales linearly at O(N) relative to the number of microservice steps.
* Space Constraints: Deduplication history stores and state tracking engines grow at O(E), where E tracks the total volume of processed domain events.