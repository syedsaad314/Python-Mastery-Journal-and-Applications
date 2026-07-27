# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: In-Place Binary Packing via struct.pack_into
Description: Serializes low-level binary data directly into pre-allocated 
             mutable memoryview buffers, eliminating binary string creation.
"""
import struct

class InPlaceStructPacker:
    @staticmethod
    def pack_header_in_place(target_buffer: bytearray, offset: int, magic: int, length: int, ratio: float) -> int:
        # Format specifier: ! (Big-Endian) H (unsigned short 2B) I (unsigned int 4B) d (double 8B) = 14 Bytes
        struct.pack_into("!HId", target_buffer, offset, magic, length, ratio)
        return struct.calcsize("!HId")

    @staticmethod
    def unpack_header_from_view(buffer_view: memoryview, offset: int) -> tuple[int, int, float]:
        return struct.unpack_from("!HId", buffer_view, offset)

if __name__ == "__main__":
    preallocated_memory = bytearray(64)
    written_bytes = InPlaceStructPacker.pack_header_in_place(
        target_buffer=preallocated_memory, 
        offset=10, 
        magic=0x4A4B, 
        length=2048, 
        ratio=0.9912
    )
    assert written_bytes == 14
    
    view = memoryview(preallocated_memory)
    magic_out, len_out, ratio_out = InPlaceStructPacker.unpack_header_from_view(view, 10)
    
    assert magic_out == 0x4A4B
    assert len_out == 2048
    assert abs(ratio_out - 0.9912) < 1e-6
    print(f"[TASK 05 PASSED] In-place binary struct serialization completed cleanly without allocation.")