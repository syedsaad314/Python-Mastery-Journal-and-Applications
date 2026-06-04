"""
Core Topic: Inter-Runtime Callback Functions
Description: Generates standard native C function pointers that route back to Python callables.
Lead Engineer: Syed Saad Bin Irfan
"""

import ctypes
import sys

# Define a prototype signature for the callback function
# Format: CFUNCTYPE(return_type, parameter_type_1, parameter_type_2)
COMPARE_CALLBACK_PROTOTYPE = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

def python_sorting_comparator_logic(pointer_a, pointer_b) -> int:
    """Custom sorting logic designed to handle native pointer comparisons directly."""
    # Extract values from the incoming pointers
    val_a = pointer_a.contents.value
    val_b = pointer_b.contents.value
    
    print(f"  [PYTHON CALLBACK INTERCEPT] Evaluating: {val_a} vs {val_b}")
    if val_a < val_b:
        return -1
    elif val_a > val_b:
        return 1
    return 0

if __name__ == "__main__":
    # Dynamically locate the system standard library based on host OS
    lib_name = "msvcrt.dll" if sys.platform.startswith("win32") else "libc.so.6"
    libc = ctypes.CDLL(lib_name)

    # Instantiate the native C function pointer mapping to our Python logic
    c_valid_callback = COMPARE_CALLBACK_PROTOTYPE(python_sorting_comparator_logic)

    # Initialize a native C integer array using ctypes multiplication syntax
    native_integer_array_type = ctypes.c_int * 4
    array_instance = native_integer_array_type(45, 12, 89, 23)

    print("[CALLBACK-CORE] Array contents pre-execution: ", [x for x in array_instance])
    print("[CALLBACK-CORE] Binding signatures and executing standard C 'qsort' routing pipeline...")

    # Configure signatures for the standard C quicksort function
    libc.qsort.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t, COMPARE_CALLBACK_PROTOTYPE]
    libc.qsort.restype = None

    # Trigger native quicksort, passing the array, length, element size, and our Python callback pointer
    libc.qsort(array_instance, 4, ctypes.sizeof(ctypes.c_int), c_valid_callback)

    print("[CALLBACK-CORE] Sorting pipeline complete. Sorted native array: ", [x for x in array_instance])