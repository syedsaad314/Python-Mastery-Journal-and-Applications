# Logic Breakdown: High-Performance Asof Joins
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
High-frequency streams (financial ticks, IoT telemetry) rarely share exact timestamps. Traditional inner or left joins fail to match records across asynchronous time series.

## My Approach
I implemented Polars `join_asof()` with `strategy="backward"`. Polars uses binary search algorithms across pre-sorted time series arrays to match each trade timestamp to the most recent quote timestamp (`quote.timestamp <= trade.timestamp`).

## Complexity Profile
* Runtime Bounds: $O(M \log N)$ where $M$ is trade count and $N$ is quote count.
* Space Constraints: $O(M)$ output memory allocation.