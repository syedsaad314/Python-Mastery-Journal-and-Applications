# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Base-128 Varint Stream Decoder
Description: Parses stream arrays chunk by chunk, processing bit offsets 
             until encountering a clean MSB marker.
"""

class VarintDecoder:
    @staticmethod
    def decode_stream(buffer: bytes) -> tuple[int, int]:
        accumulator = 0
        bit_shift = 0
        total_bytes_processed = 0
        
        for byte in buffer:
            total_bytes_processed += 1
            accumulator |= (byte & 0x7F) << bit_shift
            if not (byte & 0x80):  # Check if MSB is clean (0)
                return accumulator, total_bytes_processed
            bit_shift += 7
            
        raise ValueError("Malformed stream payload: MSB remains open indefinitely.")

if __name__ == "__main__":
    raw_payload = b'\xAC\x02'
    val, read_bytes = VarintDecoder.decode_stream(raw_payload)
    assert val == 300 and read_bytes == 2
    print(f"[TASK 02 PASSED] Successfully decoded Varint payload to integer: {val}")