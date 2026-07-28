# Logic Breakdown: Automated Memory Downcasting & Profiling
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
By default, Pandas assigns 64-bit data types (`int64`, `float64`) and Python object pointers (`object`) to read data. In large datasets, object pointers consume massive memory overhead due to Python heap allocations per string element.

## My Approach
I engineered an automated optimization pass. Integer and float columns are downcasted using `pd.to_numeric(..., downcast=...)` to fit within 8, 16, or 32-bit boundaries based on value ranges. Low-cardinality string columns (where unique ratio < 50%) are converted to `category`, storing unique strings once in an internal dictionary and replacing column data with integer codes.

## Complexity Profile
* Runtime Bounds: $O(N \cdot M)$ over $N$ rows and $M$ columns during scan pass.
* Space Constraints: Reduces overall RAM footprint up to 80% without data loss.