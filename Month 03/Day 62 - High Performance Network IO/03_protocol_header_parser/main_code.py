# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Custom Protocol Network Header Parser
Description: Decodes fixed-width custom protocol frames (Magic Byte + Payload Length) 
             from incoming raw TCP data streams.
"""
import struct

class CustomProtocolHeaderParser:
    # Topography: 1 Byte Magic Identifier (0xAA) + 4 Byte Big-Endian Unsigned Length Indicator
    HEADER_SIZE_BYTES = 5
    MAGIC_TOKEN = 0xAA

    @staticmethod
    def parse_inbound_header(raw_buffer: bytes) -> int:
        if len(raw_buffer) < CustomProtocolHeaderParser.HEADER_SIZE_BYTES:
            raise ValueError("Insufficient byte cluster size to resolve standard protocol frame metadata.")
            
        magic_byte, payload_length = struct.unpack("!BI", raw_buffer[:CustomProtocolHeaderParser.HEADER_SIZE_BYTES])
        
        if magic_byte != CustomProtocolHeaderParser.MAGIC_TOKEN:
            raise ValueError("Protocol violation: Received packet signature does not match engine standards.")
            
        return payload_length

if __name__ == "__main__":
    valid_test_stream = b'\xAA\x00\x00\x00\x20' # Magic 0xAA, Length: 32 Bytes
    extracted_length = CustomProtocolHeaderParser.parse_inbound_header(valid_test_stream)
    assert extracted_length == 32
    print(f"[TASK 03 PASSED] Header parsed perfectly. Extracted payload allocation size: {extracted_length} Bytes")