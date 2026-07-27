# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Zero-Copy Byte Slicing via C-Buffer Protocol
Description: Demonstrates zero-copy memory slicing using Python's memoryview wrapper,
             bypassing heap allocations incurred by standard byte slicing.
"""

class ZeroCopyMemorySlicing:
    @staticmethod
    def slice_without_copy(source_buffer: bytearray, start_offset: int, end_offset: int) -> memoryview:
        if not (0 <= start_offset <= end_offset <= len(source_buffer)):
            raise IndexError("Requested slicing offset boundaries fall out of buffer limits.")
            
        # Wrap raw C-buffer layout without allocating a secondary heap object
        base_view = memoryview(source_buffer)
        return base_view[start_offset:end_offset]

if __name__ == "__main__":
    underlying_data = bytearray(b"HEADER_FLAGS:0xAF91|PAYLOAD_BODY:CRITICAL_SYSTEM_STATE")
    sliced_view = ZeroCopyMemorySlicing.slice_without_copy(underlying_data, 13, 19)
    
    # Mutating the underlying bytearray alters the sliced memoryview instantly (zero-copy proof)
    assert sliced_view.tobytes() == b"0xAF91"
    underlying_data[13:19] = b"0x0000"
    assert sliced_view.tobytes() == b"0x0000"
    
    print(f"[TASK 01 PASSED] Zero-copy memory view successfully slice-bound to target: {sliced_view.tobytes()}")