# Asynchronous Choreography Saga & Transactional Outbox Engine

An enterprise-grade, decentralized transactional processing engine designed to coordinate distributed microservice workflows using autonomous event streams, transaction isolation layers, and automatic rollback routines.

## System Features
* **Decentralized Choreography Flow Control**: Eliminates single points of failure by replacing traditional orchestrators with dynamic pub/sub messaging channels.
* **Dual-Write Protection (Transactional Outbox)**: Guarantees eventual consistency by joining local state mutations and outbound events into a single atomic commit.
* **Network-Safe Consumers**: Includes input deduplication guards to prevent duplicate mutations during message redeliveries.