"""
Core Topic: Unmanaged Native Memory Lifecycles
Description: Allocates and destroys raw heap memory frames directly using C standard functions.
Lead Engineer: Syed Saad Bin Irfan
"""

import ctypes
import sys

class UnmanagedHeapBuffer:
    """Allocates and tracks explicit unmanaged system heap buffers safely."""
    def __init__(self, size_bytes: int) -> None:
        self.lib_name = "msvcrt.dll" if sys.platform.startswith("win32") else "libc.so.6"
        self.libc = ctypes.CDLL(self.lib_name)
        self.allocation_size = size_bytes
        
        # Enforce strict function definitions on native memory allocators
        self.libc.malloc.argtypes = [ctypes.c_size_t]
        self.libc.malloc.restype = ctypes.c_void_p
        self.libc.free.argtypes = [ctypes.c_void_p]
        self.libc.free.restype = None

        # Allocate unmanaged memory block on the system heap
        self.raw_memory_address = self.libc.malloc(self.allocation_size)
        if not self.raw_memory_address:
            raise MemoryError("System heap memory allocation step failed.")
        logging_id = self.raw_memory_address
        print(f"[HEAP] Allocated {self.allocation_size} bytes at memory address: {hex(logging_id)}")

    def commit_string_payload(self, text_payload: str) -> None:
        """Writes text directly to the raw unmanaged memory block using memmove."""
        encoded_bytes = text_payload.encode('utf-8')
        if len(encoded_bytes) > self.allocation_size:
            raise ValueError("Payload size breaches allocated heap buffer limits.")
        
        # Copy raw bytes into our unmanaged heap memory block
        ctypes.memmove(self.raw_memory_address, encoded_bytes, len(encoded_bytes))

    def release_buffer_safely(self) -> None:
        """Manually frees the unmanaged heap buffer block back to the operating system."""
        if self.raw_memory_address:
            logging_id = self.raw_memory_address
            self.libc.free(self.raw_memory_address)
            print(f"[HEAP] Unmanaged memory address {hex(logging_id)} successfully freed.")
            self.raw_memory_address = None

    def __del__(self) -> None:
        """Defensive fallback hook to clear memory allocations if the object is garbage collected."""
        if self.raw_memory_address is not None:
            self.release_buffer_safely()

if __name__ == "__main__":
    print("[RUN] Instantiating unmanaged raw memory allocation buffers...")
    heap_buffer = UnmanagedHeapBuffer(size_bytes=128)
    
    heap_buffer.commit_string_payload("DCS-UBIT-METRICS-CORE-DATA")
    
    # Extract string from raw pointer address to verify the update
    extracted_string = ctypes.string_at(heap_buffer.raw_memory_address)
    print(f"[RUN] Successfully extracted data from heap segment address: {extracted_string.decode('utf-8')}")
    
    heap_buffer.release_buffer_safely()