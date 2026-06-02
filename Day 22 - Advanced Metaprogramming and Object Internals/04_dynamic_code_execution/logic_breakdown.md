# Logic Breakdown: Isolated Dynamic Code Execution
**Engineer:** Syed Saad Bin Irfan

## The Problem
Executing dynamic mathematical expressions provided by users at runtime can open severe security holes if malicious payloads (like commands to wipe server drives) slip through unverified.

## My Approach
I implemented a secure, isolated sandboxing environment using Python's `compile()` and `eval()` functions. 

The approach relies on complete namespace isolation. By explicitly setting the global scope container to `{"__builtins__": None}`, the code is stripped of access to dangerous functions like `__import__` or `open()`. Only trusted variables are injected into the local scope, allowing users to execute dynamic math calculations safely without risking server compromises.

## Complexity Profile
* **Runtime Bounds:** Bytecode compilation runs in linear $O(S)$ time relative to string length; evaluation speed is constant $O(1)$.
* **Space Constraints:** Minimal local dictionary scope allocation variables.