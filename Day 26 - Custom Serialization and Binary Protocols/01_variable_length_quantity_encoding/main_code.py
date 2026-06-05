"""
Core Topic: Variable-Length Quantity (VLQ / LEB128 Varint) Serialization
Description: Implements space-efficient variable-length integer compaction used by Protocol Buffers.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Tuple

class VarintCodec:
    """Encodes and decodes unsigned 64-bit integers using Little-Endian Base 128 compression mechanics."""
    
    @staticmethod
    def encode(number: int) -> bytes:
        """Squeezes an integer down into a minimized byte array based on numerical value scale."""
        if number < 0:
            raise ValueError("Varint codec implementation limited to unsigned integers only.")
        
        output_buffer = bytearray()
        while True:
            # Isolate the lowest 7 bits of the integer value
            lowest_seven_bits = number & 0x7F
            number >>= 7
            if number != 0:
                # Set the most significant bit (MSB) high to signal subsequent bytes are arriving
                output_buffer.append(lowest_seven_bits | 0x80)
            else:
                # Clear the MSB to signal termination of the variable length payload sequence
                output_buffer.append(lowest_seven_bits)
                break
        return bytes(output_buffer)

    @staticmethod
    def decode(buffer_bytes: bytes, start_offset: int = 0) -> Tuple[int, int]:
        """Parses a packed byte array stream to extract the integer value and its read offset length."""
        accumulated_value = 0
        bit_shift_offset = 0
        current_index = start_offset

        while current_index < len(buffer_bytes):
            byte_payload = buffer_bytes[current_index]
            current_index += 1
            
            # Mask out the continuation bit (MSB) and shift the remaining 7 bits into the value
            accumulated_value |= (byte_payload & 0x7F) << bit_shift_offset
            
            # Check if the continuation bit is clear, signaling the end of the varint
            if not (byte_payload & 0x80):
                bytes_consumed = current_index - start_offset
                return accumulated_value, bytes_consumed
                
            bit_shift_offset += 7
            if bit_shift_offset >= 64:
                raise OverflowError("Varint decoding loop detected a malformed data payload size anomaly.")
                
        raise IndexError("Incomplete byte stream encountered during varint deserialization.")


if __name__ == "__main__":
    print("[VARINT-CODEC] Initializing compression metrics evaluation pass...")
    
    # Test cases: small numbers should take 1 byte; large numbers scale up dynamically
    test_integers = [42, 300, 202611, 4294967295]
    
    for val in test_integers:
        encoded_bytes = VarintCodec.encode(val)
        decoded_val, bytes_used = VarintCodec.decode(encoded_bytes)
        
        print(f" Integer: {val:<12} -> Packed Size: {len(encoded_bytes)} bytes | Verified Result: {decoded_val}")
        assert val == decoded_val