# Logic Breakdown: Physical Clock Skew and Drift Simulator
**Engineer:** Syed Saad Bin Irfan

## The Problem
Hardware quartz crystals tick at slightly different rates due to temperature changes and manufacturing differences. If a system relies entirely on wall-clock time (`time.time()`) to order database writes, an update processed by a fast clock could accidentally overwrite a newer update processed by a slow clock.

## My Approach
I built a **Clock Drift Simulation Model** to showcase this vulnerability.

By configuring two nodes with artificial clock offsets (+5 seconds and -5 seconds), we simulate real-world clock drift. When a transaction occurs on the slower node first and a subsequent transaction runs on the faster node second, sorting them by wall-clock time completely flips their actual sequence. This proves why logical boundaries or specialized hardware (like TrueTime GPS synchronized systems) are essential for data consistency.

## Complexity Profile
* **Runtime Bounds:** Generating timestamps and logging entries runs in $O(1)$ constant time.
* **Space Constraints:** Scales at $O(T)$ linear memory complexity relative to the total number of logged transactions $T$.