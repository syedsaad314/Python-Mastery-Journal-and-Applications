# Logic Breakdown: Parallel Expression Vectorization
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Using `.apply()` with Python lambda callbacks forces context switches between Rust/C engine internals and the Python GIL interpreter loop, single-threading execution and degrading processing speeds.

## My Approach
I utilized Polars' native Expression API (`pl.when()`, `pl.col()`, `.alias()`). Expressions represent declarative AST nodes passed down to the Polars core engine, enabling automatic multi-threading across physical CPU cores via Rayon.

## Complexity Profile
* Runtime Bounds: $O(N / T)$ where $N$ is row count and $T$ is available CPU worker threads.
* Space Constraints: $O(N)$ memory layout with contiguous memory allocations.