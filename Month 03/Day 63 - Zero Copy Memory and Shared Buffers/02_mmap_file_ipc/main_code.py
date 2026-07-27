# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Memory-Mapped File I/O Engine
Description: Maps disk files directly into process virtual memory space using OS kernel mmap,
             enabling ultra-fast random access and cross-process file IPC.
"""
import mmap
import os

class MemoryMappedIOEngine:
    @staticmethod
    def initialize_and_write_mmap(filepath: str, payload: bytes) -> bytes:
        payload_size = len(payload)
        
        # Pre-allocate file size on disk before mapping
        with open(filepath, "wb") as file_handle:
            file_handle.write(b"\x00" * payload_size)
            
        with open(filepath, "r+b") as file_handle:
            # Map file descriptor directly into process memory addresses
            with mmap.mmap(file_handle.fileno(), payload_size, access=mmap.ACCESS_WRITE) as mmap_obj:
                mmap_obj[0:payload_size] = payload
                mmap_obj.flush()
                
            # Re-open in read mode to verify mapped byte persistence
            with mmap.mmap(file_handle.fileno(), payload_size, access=mmap.ACCESS_READ) as read_mmap:
                return read_mmap[:]

if __name__ == "__main__":
    temp_file = "mmap_test_buffer.tmp"
    test_payload = b"SYSTEM_TELEMETRY_LOG_ENTRY_HEX_883921"
    
    try:
        read_back = MemoryMappedIOEngine.initialize_and_write_mmap(temp_file, test_payload)
        assert read_back == test_payload
        print(f"[TASK 02 PASSED] Memory-mapped file I/O executed cleanly. Persisted bytes: {len(read_back)}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)