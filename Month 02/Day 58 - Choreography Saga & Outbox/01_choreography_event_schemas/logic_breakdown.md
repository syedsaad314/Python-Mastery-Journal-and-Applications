# Logic Breakdown: Choreography Event Schemas
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
In an event-driven choreography saga, there is no master orchestrator directing traffic. Microservices communicate exclusively via an asynchronous event stream. If these event schemas are loose, malformed, or mutable, downstream consumers will crash, creating silent black holes across your distributed system.

## My Approach
I utilized Python's `@dataclass(frozen=True)` pattern to construct strictly immutable domain event structures. Each event carries a mandatory `correlation_id` that ties asynchronous requests and responses together across different microservice contexts.

## Complexity Profile
* Runtime Bounds: Event object allocation runs in constant O(1) time.
* Space Constraints: Memory allocation is restricted to a tight O(1) footprint per transaction token.