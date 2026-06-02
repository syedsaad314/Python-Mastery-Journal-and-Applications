# Portfolio Code Review: Code Auditor and Complexity Profiler
**Author:** Syed Saad Bin Irfan

## Practical Context
This static code analyzer serves as an automated security check for CI/CD pipelines, analyzing abstract syntax tree structures to catch software vulnerabilities and complexity issues before deployment.

## Engineering Standards Applied
* **AST Structural Auditing:** Uses Python's `ast.NodeVisitor` framework to explore code structure reliably, avoiding the false positives common in simple text-matching approaches.
* **Complexity Density Analysis:** Measures function complexity by tracking structural code branches (`If`, `While`, `For`), highlighting dense, hard-to-maintain code blocks automatically.
* **Isolated Security Guardrails:** Scans active code nodes to flag insecure operations like `eval()`, helping teams enforce secure coding standards across large enterprise software architectures.