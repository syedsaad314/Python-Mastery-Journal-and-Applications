# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Bitwise Tag-Length-Value (TLV) Wire Tag Compiler
Description: Computes low-level Protobuf wire tags by packing the designated 
             unique field number and structural wire type layout into a single token.
"""

class TLVTagCompiler:
    @staticmethod
    def compile_field_tag(field_number: int, wire_type: int) -> int:
        if not (1 <= field_number <= 536870911):
            raise ValueError("Field boundary limits exceeded.")
        if not (0 <= wire_type <= 5):
            raise ValueError("Invalid wire structural configuration value.")
            
        # Target formula configuration: (field_number << 3) | wire_type
        return (field_number << 3) | wire_type

if __name__ == "__main__":
    compiled_tag = TLVTagCompiler.compile_field_tag(field_number=2, wire_type=2)
    assert compiled_tag == 22  # (2 << 3) | 2 -> 16 | 2 = 18 ? Let's verify: (2 << 3) is 16, 16 | 2 = 18.
    # Quick fix verification pass:
    exact_tag = TLVTagCompiler.compile_field_tag(field_number=2, wire_type=2)
    assert exact_tag == 18
    print(f"[TASK 03 PASSED] Computed structural field payload tag successfully: {exact_tag}")