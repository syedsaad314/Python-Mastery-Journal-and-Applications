"""
Core Topic: Type-Length-Value (TLV) Binary Framing Protocol
Description: Implements structured network data framing with clean boundary tracking.
Lead Engineer: Syed Saad Bin Irfan
"""

import struct
from typing import NamedTuple, Tuple

class TLVFrame(NamedTuple):
    type_tag: int
    length: int
    value: bytes

class TLVFramerEngine:
    """Handles parsing and extraction operations across Type-Length-Value data payloads."""
    # Wire structure format signature: uint8 (Type), uint16 (Length) in Network Big-Endian order
    HEADER_FORMAT = "!BH"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    @classmethod
    def compile_frame(cls, type_tag: int, value_bytes: bytes) -> bytes:
        """Packs variables cleanly into a standard binary TLV network frame structure."""
        length_val = len(value_bytes)
        # Pack the header properties and append the raw data array
        header = struct.pack(cls.HEADER_FORMAT, type_tag, length_val)
        return header + value_bytes

    @classmethod
    def deconstruct_single_frame(cls, stream_buffer: bytes, offset: int = 0) -> Tuple[TLVFrame, int]:
        """Parses a structured data block to extract the first valid TLV network frame."""
        if len(stream_buffer) - offset < cls.HEADER_SIZE:
            raise ValueError("Buffer frame size lacks required header metadata tracking limits.")
            
        # Extract the type tag and length from the frame header block
        type_tag, length_val = struct.unpack_from(cls.HEADER_FORMAT, stream_buffer, offset)
        
        data_start_pos = offset + cls.HEADER_SIZE
        data_end_pos = data_start_pos + length_val
        
        if len(stream_buffer) < data_end_pos:
            raise IndexError("Incomplete buffer stream encountered during payload decoding.")
            
        value_payload = stream_buffer[data_start_pos:data_end_pos]
        return TLVFrame(type_tag, length_val, value_payload), data_end_pos


if __name__ == "__main__":
    print("[TLV-ENGINE] Starting binary framing orchestration runs...")
    
    raw_message_bytes = b"UBIT_NODE_METRIC_VALUE_STABLE"
    packed_packet = TLVFramerEngine.compile_frame(type_tag=0xA5, value_bytes=raw_message_bytes)
    print(f"[TLV-ENGINE] Compiled wire packet length: {len(packed_packet)} total bytes allocation.")

    frame, next_offset = TLVFramerEngine.deconstruct_single_frame(packed_packet)
    print(f"[TLV-ENGINE] Decoded Frame -> Tag: {hex(frame.type_tag)} | Len: {frame.length} | Body: {frame.value.decode()}")