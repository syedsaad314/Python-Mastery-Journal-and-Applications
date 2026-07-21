# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Base-128 Variable-Length Quantity (Varint) Encoder
Description: Implements low-level bitwise shifting to compress variable integers. 
             Sets the Most Significant Bit (MSB) to indicate trailing data segments.
"""

class VarintEncoder:
    @staticmethod
    def encode_unsigned(value: int) -> bytes:
        if value < 0:
            raise ValueError("This encoder treats unsigned positive integers only.")
        if value == 0:
            return b'\x00'
        
        buffer = bytearray()
        while value > 0:
            byte_segment = value & 0x7F  # Extract lowest 7 bits
            value >>= 7                 # Shift right to inspect next group
            if value > 0:
                byte_segment |= 0x80    # Flip MSB to 1: more bytes are coming
            buffer.append(byte_segment)
        return bytes(buffer)

if __name__ == "__main__":
    encoded = VarintEncoder.encode_unsigned(300)
    assert encoded == b'\xAC\x02'
    print(f"[TASK 01 PASSED] Encoded integer 300 to Varint Hex: {encoded.hex().upper()}")