"""
System: Code Auditor and Complexity Profiler
Description: A security linter that reviews script code files, analyzes abstract syntax trees (AST) 
             for vulnerabilities, and logs performance metrics.
Lead Engineer: Syed Saad Bin Irfan
"""

import ast
import json
import time
from typing import Dict, Any, List

class CodebaseAuditorEngine(ast.NodeVisitor):
    """AST code explorer that scans source code syntax arrays to flag security flaws and quality metrics."""
    def __init__(self) -> None:
        self.audit_report: Dict[str, Any] = {
            "banned_functions_detected": [],
            "total_function_definitions": 0,
            "complexity_score_estimate": 0
        }

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Counts defined functions and monitors local complexity metrics."""
        self.audit_report["total_function_definitions"] += 1
        
        # Calculate a basic structural complexity estimate by counting logic branches inside the function
        branch_density = 0
        for sub_node in ast.walk(node):
            if isinstance(sub_node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                branch_density += 1
                
        self.audit_report["complexity_score_estimate"] += branch_density
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Intercepts evaluation calls statement nodes to flag dangerous function strings."""
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
            if function_name in ["eval", "exec", "compile"]:
                log_entry = f"BANNED_CALL_WARNING::'{function_name}' deployed at line number {node.lineno}"
                self.audit_report["banned_functions_detected"].append(log_entry)
        self.generic_visit(node)


class CodeProfilerService:
    @staticmethod
    def audit_and_profile_source(raw_python_source: str) -> Dict[str, Any]:
        """Parses a source text script, runs security analysis over its AST, and metrics performance profile."""
        start_timestamp = time.perf_counter()
        
        # Step 1: Parse the source string into an Abstract Syntax Tree graph layout
        syntax_tree_root = ast.parse(raw_python_source)
        
        # Step 2: Run the syntax analysis linter pass
        inspector = CodebaseAuditorEngine()
        inspector.visit(syntax_tree_root)
        
        # Step 3: Measure execution overhead costs accurately
        total_processing_duration = time.perf_counter() - start_timestamp
        
        final_summary = inspector.audit_report
        final_summary["audit_processing_time_sec"] = round(total_processing_duration, 6)
        return final_summary


if __name__ == "__main__":
    print("\n=== SYSTEM START: PRODUCTION-GRADE CODE AUDITOR AND LINTER ===\n")

    # Mock codebase payload string designed to simulate dynamic structural checks
    target_codebase_sample = (
        "def process_user_login(username, input_password_hash):\n"
        "    if not username or not input_password_hash:\n"
        "        return False\n"
        "    print('Logging user in...!')\n"
        "    return True\n\n"
        "def dynamic_calculation_pipeline(user_code_string):\n"
        "    # Intentional safety flaws to test code auditor capabilities\n"
        "    sanitized_output = eval(user_code_string)\n"
        "    for item in range(10):\n"
        "        print(item)\n"
        "    return sanitized_output\n"
    )

    print("[PROFILER] Running static analysis and structural audits over target codebase string...")
    insights_summary = CodeProfilerService.audit_and_profile_source(target_codebase_sample)
    
    print("\n=== SECURITY AUDIT METRICS PAYLOAD ===")
    print(json.dumps(insights_summary, indent=4))