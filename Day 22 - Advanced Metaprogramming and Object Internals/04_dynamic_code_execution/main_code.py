"""
Core Topic: Isolated Dynamic Code Execution
Description: Compiles and runs arbitrary code blocks within sandboxed namespace dictionaries.
Lead Engineer: Syed Saad Bin Irfan
"""

class DynamicSandboxExecutor:
    @staticmethod
    def execute_sandboxed_calculation(expression_string: str, input_parameter: float) -> float:
        """Compiles an expression string and executes it within an isolated namespace wrapper."""
        # Pre-compile the raw formula string into optimized system bytecode
        compiled_bytecode = compile(expression_string, "<sandbox_computation>", "eval")
        
        # Build an isolated execution namespace by blocking access to built-in functions
        isolated_globals = {"__builtins__": None}
        isolated_locals = {"x": input_parameter}
        
        try:
            execution_result = eval(compiled_bytecode, isolated_globals, isolated_locals)
            return float(execution_result)
        except TypeError as err:
            print(f"[SANDBOX BLOCKED ALERT] Malicious call attempt or typing mismatch: {err}")
            raise

if __name__ == "__main__":
    formula = "x * 2.5 + 10"
    test_input = 4.0
    
    output = DynamicSandboxExecutor.execute_sandboxed_calculation(formula, test_input)
    print(f"[SANDBOX] Input parameter X: {test_input} | Calculated Sandbox Output: {output}")

    try:
        # Attempt to run a malicious input that bypasses standard validation controls
        malicious_formula = "__import__('os').system('clear')"
        DynamicSandboxExecutor.execute_sandboxed_calculation(malicious_formula, test_input)
    except TypeError:
        print("[SANDBOX SUCCESS] Successfully blocked malicious system access attempt.")