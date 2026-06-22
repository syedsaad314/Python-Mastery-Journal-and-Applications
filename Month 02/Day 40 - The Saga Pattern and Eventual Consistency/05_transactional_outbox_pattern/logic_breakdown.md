# Logic Breakdown: Transactional Outbox Pattern
**Engineer:** Syed Saad Bin Irfan

## The Problem
A common bug in microservices is updating a local database and trying to send a message to a broker right after. If the network drops or the broker crashes mid-flight, the database change is saved but the message is lost, causing data inconsistency between services.

## My Approach
I designed a **Transactional Outbox Dual-Write Pattern**.

To guarantee that database updates and event messages stay in sync, the service saves them together to the same local database within a single atomic transaction. The change is written to the business table while the outbound event is saved to an `outbox` table. A background process then reads this outbox table to publish events reliably, ensuring messages are delivered safely even if the network drops.

## Complexity Profile
* **Runtime Bounds:** Saving the atomic local database records runs in $O(1)$ constant time.
* **Space Constraints:** The outbox buffer scales linearly at $O(M)$ with the volume of pending outbound messages $M$.