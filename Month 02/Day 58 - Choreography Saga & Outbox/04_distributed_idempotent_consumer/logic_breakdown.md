# Logic Breakdown: Distributed Idempotent Consumer Guards
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Because network delivery models like the Outbox pattern favor "at-least-once" delivery, retries are inevitable. If a broker drops an acknowledgment, it will redeliver the exact same event. Without an active safety check, consumers will repeat state changes, corrupting things like financial balances or inventory counts.

## My Approach
I put an idempotency guard at the consumer entryway. The system checks each incoming message ID against a deduplication store. If the ID is recognized, it drops the message immediately and returns a safe success status without re-running the underlying logic.

## Complexity Profile
* Runtime Bounds: Checking the deduplication store runs in constant O(1) time.
* Space Constraints: Storage scales linearly at O(M) with the total volume of processed message keys.