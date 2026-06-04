"""
Core Topic: Raw Virtual Memory Pointer Manipulation and Pointer Casting
Description: Modifies raw memory content values directly via reference addresses.
Lead Engineer: Syed Saad Bin Irfan
"""

import ctypes

class MemoryAddressManipulator:
    """Handles pointer mutations and explicit data type casting across raw memory bytes."""
    @staticmethod
    def alter_value_via_pointer(target_variable: ctypes.c_int64, absolute_new_value: int) -> None:
        # Generate an explicit pointer tracking the variable's physical address location
        variable_pointer = ctypes.pointer(target_variable)
        
        print(f"[POINTER-CORE] Virtual RAM reference address location: {variable_pointer}")
        # Mutate memory contents by altering the pointer value
        variable_pointer.contents.value = absolute_new_value

    @staticmethod
    def execute_raw_void_pointer_cast(target_variable: ctypes.c_int32) -> int:
        """Casts an integer reference address to a generic void pointer and back to a 32-bit int."""
        generic_void_pointer = ctypes.cast(ctypes.pointer(target_variable), ctypes.c_void_p)
        print(f"[POINTER-CORE] Casted generic void pointer token: {generic_void_pointer.value}")
        
        # Recast the raw void pointer address back to an explicit 32-bit integer pointer
        restored_pointer = ctypes.cast(generic_void_pointer, ctypes.POINTER(ctypes.c_int32))
        return restored_pointer.contents.value

if __name__ == "__main__":
    base_data = ctypes.c_int64(4500112)
    print(f"[MAIN] Value before execution: {base_data.value}")

    MemoryAddressManipulator.alter_value_via_pointer(base_data, 7789012)
    print(f"[MAIN] Value after pointer update: {base_data.value}")

    casting_target = ctypes.c_int32(101)
    extracted_value = MemoryAddressManipulator.execute_raw_void_pointer_cast(casting_target)
    print(f"[MAIN] Restored type value after void cast step: {extracted_value}")