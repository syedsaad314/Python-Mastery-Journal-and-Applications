"""
Core Topic: Platform-Agnostic Native Shared Library Loading
Description: Dynamically locates and binds the operating system's standard C library using ctypes.
Lead Engineer: Syed Saad Bin Irfan
"""

import ctypes
from ctypes.util import find_library
import sys

class NativeLibraryLoader:
    """Safely locates and abstracts system-level pre-compiled shared library binaries."""
    def __init__(self) -> None:
        self.lib_path = self._discover_standard_c_library()
        # Load the dynamic shared library into the application process memory space
        self.native_lib = ctypes.CDLL(self.lib_path)

    def _discover_standard_c_library(self) -> str:
        """Finds the path to the system standard library dynamically based on the current OS host."""
        if sys.platform.startswith("win32"):
            # Windows utilizes the Microsoft C Runtime library binary name mapping
            target_name = "msvcrt"
        elif sys.platform.startswith("darwin"):
            target_name = "libc.dylib"
        else:
            target_name = "c"

        resolved_path = find_library(target_name)
        if not resolved_path:
            # Fallback configuration parameter if target paths are obscured
            if sys.platform.startswith("win32"):
                return "msvcrt.dll"
            return "libc.so.6"
        return resolved_path

    def execute_native_absolute_value(self, input_integer: int) -> int:
        """Invokes the native C standard 'abs' function directly inside memory."""
        # Explicitly configure function parameter and return types to prevent segmentation faults
        self.native_lib.abs.argtypes = [ctypes.c_int]
        self.native_lib.abs.restype = ctypes.c_int
        
        return self.native_lib.abs(input_integer)

if __name__ == "__main__":
    print("[NATIVE-LOADER] Initializing FFI standard C bindings pipeline...")
    loader = NativeLibraryLoader()
    print(f"[NATIVE-LOADER] Target platform binary located at: {loader.lib_path}")
    
    test_value = -2026
    native_output = loader.execute_native_absolute_value(test_value)
    print(f"[NATIVE-LOADER] Input: {test_value} -> Computed Native 'abs' Output: {native_output}")