# Logic Breakdown: Idempotent Participant Message Handlers
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Because distributed networks can drop or delay messages, an orchestrator will often retry requests if it doesn't get a response fast enough. Without safety guards, these retries can cause participant services to duplicate actions, like charging a customer twice for the same order.

## My Approach
I designed a deduplication ledger cache inside the participant service. The service inspects an incoming unique correlation ID before running any logic. If it spots a token it already processed, it skips the execution entirely and passes back the safely cached historical response.

## Complexity Profile
* Runtime Bounds: Verifying tokens and retrieving cached responses runs in $O(1)$ constant time.
* Space Constraints: Tracking incoming requests requires linear space $O(U)$ relative to the number of unique messages.