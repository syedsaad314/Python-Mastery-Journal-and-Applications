"""
System: Low-Level Cryptographic Memory Arena and Secure Buffer Interoperability Layer
Description: Allocates memory-isolated heap buffers, processes data transforms natively, 
             and scrubs memory fields completely upon teardown to prevent data leaks.
Lead Engineer: Syed Saad Bin Irfan
"""

import ctypes
import logging
import sys
import time

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Secure-Buffer) %(message)s')

class LowLevelSecureBufferArena:
    """Allocates and protects sensitive data frames inside isolated system heap buffers."""
    def __init__(self, buffer_size_allocation: int) -> None:
        self.lib_name = "msvcrt.dll" if sys.platform.startswith("win32") else "libc.so.6"
        self.libc = ctypes.CDLL(self.lib_name)
        self.capacity = buffer_size_allocation
        
        # Define strict argument signatures for memory management functions
        self.libc.malloc.argtypes = [ctypes.c_size_t]
        self.libc.malloc.restype = ctypes.c_void_p
        self.libc.free.argtypes = [ctypes.c_void_p]
        self.libc.free.restype = None
        self.libc.memset.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_size_t]
        self.libc.memset.restype = ctypes.c_void_p

        # Secure allocation pool block on the system heap partition
        self.heap_address = self.libc.malloc(self.capacity)
        if not self.heap_address:
            raise MemoryError("Critical: Failed to isolate memory allocation block on system heap.")
            
        logging_id = self.heap_address
        logging.info(f"Isolated secure memory arena. Allocation block base address: {hex(logging_id)}")
        
        # Zero-initialize the entire buffer to clear out any stale residual data
        self.libc.memset(self.heap_address, 0, self.capacity)

    def write_confidential_payload(self, cleartext_string: str) -> int:
        """Writes data straight to the unmanaged heap arena block."""
        encoded_payload_bytes = cleartext_string.encode('utf-8')
        payload_length = len(encoded_payload_bytes)
        
        if payload_length > self.capacity:
            raise ValueError("Data scale parameters exceed isolated buffer threshold capacities.")

        # Copy data bytes directly into our unmanaged heap buffer memory block
        ctypes.memmove(self.heap_address, encoded_payload_bytes, payload_length)
        return payload_length

    def execute_native_xor_obfuscation(self, key_mask_byte: int) -> None:
        """Applies a high-speed bitwise XOR transformation directly across the unmanaged buffer values."""
        # Cast the raw memory address pointer to a workable array configuration layout
        data_view_pointer = ctypes.cast(self.heap_address, ctypes.POINTER(ctypes.c_ubyte))
        
        logging.info(f"Running bitwise XOR transformation natively across memory addresses...")
        for idx in range(self.capacity):
            # Apply bitwise masks directly to data elements inside memory
            current_byte = data_view_pointer[idx]
            if current_byte != 0:  # Skip zero-initialized padding elements
                data_view_pointer[idx] = current_byte ^ key_mask_byte

    def extract_current_arena_bytes(self) -> bytes:
        """Extracts the current raw byte payload contents out from the unmanaged memory space."""
        return ctypes.string_at(self.heap_address, self.capacity)

    def scrub_and_terminate_arena(self) -> None:
        """Overwrites memory with zeroes to secure content fields before returning the buffer to the OS."""
        if self.heap_address:
            logging_id = self.heap_address
            logging.info(f"Initiating security scrub pass on memory sector: {hex(logging_id)}")
            
            # Completely overwrite the entire buffer with zeroes to resist cold-boot memory inspections
            self.libc.memset(self.heap_address, 0, self.capacity)
            
            # Free the unmanaged memory block back to the operating system pool
            self.libc.free(self.heap_address)
            self.heap_address = None
            logging.info("Secure arena dismantled. Memory returned to OS pool.")

    def __del__(self) -> None:
        """Automated destruction fallback guard to prevent unmanaged resource leaks."""
        if self.heap_address is not None:
            self.scrub_and_terminate_arena()


if __name__ == "__main__":
    print("\n=== SYSTEM START: DISTRIBUTED NATIVE SECURE STORAGE ARENA ===\n")
    
    # Isolate a 32-byte memory arena block
    arena = LowLevelSecureBufferArena(buffer_size_allocation=32)

    confidential_data = "SaadSecretToken2026"
    arena.write_confidential_payload(confidential_data)
    print(f"[ARENA LOG] Data committed to memory. Current raw contents: {arena.extract_current_arena_bytes()}")

    # Apply a bitwise XOR rotation transformation natively across memory values
    mask_key = 0x5A
    arena.execute_native_xor_obfuscation(mask_key)
    print(f"[ARENA LOG] Post-obfuscation raw byte array contents: {arena.extract_current_arena_bytes()}")

    # Re-apply the bitwise XOR rotation to reverse the transformation and restore the plaintext data
    arena.execute_native_xor_obfuscation(mask_key)
    print(f"[ARENA LOG] Reversed transformation output: {arena.extract_current_arena_bytes().decode('utf-8').strip(chr(0))}")

    # Completely scrub and dismantle the memory arena space safely
    arena.scrub_and_terminate_arena()