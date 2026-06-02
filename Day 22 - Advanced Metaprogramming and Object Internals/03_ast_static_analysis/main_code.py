"""
Core Topic: Abstract Syntax Tree (AST) Source Inspection
Description: Parses raw code blocks into structural components to audit and block dangerous functions.
Lead Engineer: Syed Saad Bin Irfan
"""

import ast

class SecurityAuditVisitor(ast.NodeVisitor):
    """AST node explorer that flags occurrences of blacklisted functions like eval."""
    def __init__(self) -> None:
        self.violations_found: int = 0

    def visit_Call(self, node: ast.Call) -> None:
        # Check if the node matches a direct function execution call statement
        if isinstance(node.func, ast.Name):
            function_identifier = node.func.id
            if function_identifier in ["eval", "exec"]:
                print(f"[SECURITY ALERT] Discovered banned call statement: '{function_identifier}' at line {node.lineno}")
                self.violations_found += 1
        # Continue traversing the remaining child nodes down the abstract syntax tree
        self.generic_visit(node)


if __name__ == "__main__":
    source_payload = (
        "def evaluate_metrics(data_stream):\n"
        "    print('Processing logs...')\n"
        "    result_value = eval(data_stream) # Dangerous structural inclusion point\n"
        "    return result_value\n"
    )

    print("[AST MODULE] Constructing an Abstract Syntax Tree from raw source strings...")
    syntax_tree_root = ast.parse(source_payload)
    
    auditor = SecurityAuditVisitor()
    auditor.visit(syntax_tree_root)
    
    print(f"[AST MODULE] Code auditing finished. Total security alerts raised: {auditor.violations_found}")