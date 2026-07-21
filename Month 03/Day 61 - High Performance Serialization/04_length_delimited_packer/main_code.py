# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Length-Delimited Binary Content Packaging
Description: Packs complex vector payloads (strings, raw nested bytes) 
             by prefixing data streams with a Varint-encoded size array descriptor.
"""
from varint_encoder.main_code import VarintEncoder # type: ignore

class LengthDelimitedPacker:
    @staticmethod
    def pack_string(content: str) -> bytes:
        raw_bytes = content.encode('utf-8')
        length_prefix = VarintEncoder.encode_unsigned(len(raw_bytes))
        return length_prefix + raw_bytes

if __name__ == "__main__":
    packed_str = LengthDelimitedPacker.pack_string("Saad")
    assert packed_str == b'\x04Saad'
    print(f"[TASK 04 PASSED] Length-Delimited payload constructed: {packed_str}")