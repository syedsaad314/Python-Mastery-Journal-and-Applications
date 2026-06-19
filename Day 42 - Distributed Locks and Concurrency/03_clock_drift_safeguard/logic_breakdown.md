# Logic Breakdown: Clock Drift Mitigation Math
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Distributed physical system clocks cannot be perfectly synchronized. If Server A thinks 10 seconds have passed while Server B's clock runs slower, Server B might claim a lock before Server A realizes its lease has ended, breaking exclusive access guarantees.

## My Approach
I implemented a structural **Clock Drift Safe Lifetime Adjuster**.

Instead of treating the raw Lease TTL as a precise window, the coordinator mathematically shrinks the usable lifetime of the lock using the formula:

$$\text{Effective\_TTL} = \text{Total\_TTL} - \text{Drift\_Error} - \text{Processing\_Divergence}$$

By subtracting the maximum potential clock drift, the system guarantees the lock holder safely finishes or yields before another node can attempt to claim the resource.

## Complexity Profile
* **Runtime Bounds:** Arithmetic validation adjustments evaluate in $O(1)$ constant time.
* **Space Constraints:** Operates within $O(1)$ constant tracking space boundaries.