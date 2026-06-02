# Logic Breakdown: Abstract Syntax Tree (AST) Source Inspection
**Engineer:** Syed Saad Bin Irfan

## The Problem
Scanning source code files for dangerous functions like `eval()` using basic string matching or regular expressions is unreliable because keywords inside string literals or comments can easily trigger false positives.

## My Approach
I utilized Python's built-in `ast` module to break source text down into a reliable **Abstract Syntax Tree (AST)** structural graph.

By extending the `ast.NodeVisitor` class and overriding the `visit_Call` hook, the engine filters out comments and variables, focusing entirely on active function calls. This lets you audit code safety with complete structural accuracy, providing a solid foundation for custom code linters and automated static analysis tools.

## Complexity Profile
* **Runtime Bounds:** Bounded linearly at $O(L)$ where $L$ matches overall source character length.
* **Space Constraints:** Scales at $O(N)$ memory allocations to house parsed tree nodes maps.