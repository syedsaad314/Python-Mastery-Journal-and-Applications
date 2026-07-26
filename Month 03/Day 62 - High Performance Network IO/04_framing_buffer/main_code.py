# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Stream Framing Accumulator Buffer
Description: Manages TCP stream fragmentation ("sticky packets") by buffering 
             partial data chunks until complete frames can be extracted.
"""
import struct

class StreamFramingBuffer:
    def __init__(self):
        self._internal_accumulator = bytearray()

    def append_chunk(self, data: bytes) -> None:
        self._internal_accumulator.extend(data)

    def extract_next_frame(self) -> bytes | None:
        # Check if enough bytes exist to read the 5-byte header
        if len(self._internal_accumulator) < 5:
            return None
            
        magic, expected_len = struct.unpack("!BI", self._internal_accumulator[:5])
        total_frame_size = 5 + expected_len
        
        # Verify the complete payload has arrived in the system buffer
        if len(self._internal_accumulator) < total_frame_size:
            return None
            
        # Extract the complete packet and trim the buffer
        complete_frame = bytes(self._internal_accumulator[5:total_frame_size])
        del self._internal_accumulator[:total_frame_size]
        return complete_frame

if __name__ == "__main__":
    stream_buffer = StreamFramingBuffer()
    # Simulating a fragmented transmission step (Header + half of payload)
    stream_buffer.append_chunk(b'\xAA\x00\x00\x00\x04He')
    assert stream_buffer.extract_next_frame() is None # Payload incomplete
    
    # Send the trailing slice of data
    stream_buffer.append_chunk(b'llo')
    extracted = stream_buffer.extract_next_frame()
    assert extracted == b'Hell'
    print(f"[TASK 04 PASSED] Framing accumulator successfully reconstituted text payload: {extracted}")