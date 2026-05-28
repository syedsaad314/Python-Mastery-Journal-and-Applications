"""
Core Topic: Binary Protocol Engineering (WebSocket Framing)
Description: Decodes binary WebSocket data frames using low-level bit shifting masks.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Tuple

class WebSocketFramer:
    @staticmethod
    def decode_client_frame(raw_binary_frame: bytes) -> Tuple[int, str]:
        """Decodes raw binary network blocks according to the RFC 6455 framing specification guidelines."""
        if len(raw_binary_frame) < 6:
            return 0, ""

        # Extract the opcode flag from the first byte block
        opcode = raw_binary_frame[0] & 0x0F
        
        # Check the payload length and mask bit flag from the second byte block
        second_byte = raw_binary_frame[1]
        is_masked = (second_byte & 0x80) != 0
        payload_len = second_byte & 0x7F

        # Base implementation assumes standard short payload sizing profiles (< 126 bytes)
        masking_key_offset = 2
        if payload_len == 126:
            masking_key_offset = 4
        elif payload_len == 127:
            masking_key_offset = 10

        unmasked_payload_chars = []
        if is_masked:
            # Extract the 4-byte key used for payload obfuscation
            mask_key = raw_binary_frame[masking_key_offset : masking_key_offset + 4]
            data_start_offset = masking_key_offset + 4
            
            # Decode payload bytes by applying a cyclic XOR operation with the mask key
            for idx, byte_val in enumerate(raw_binary_frame[data_start_offset:]):
                unmasked_byte = byte_val ^ mask_key[idx % 4]
                unmasked_payload_chars.append(chr(unmasked_byte))
        else:
            data_start_offset = masking_key_offset
            for byte_val in raw_binary_frame[data_start_offset:]:
                unmasked_payload_chars.append(chr(byte_val))

        return opcode, "".join(unmasked_payload_chars)

if __name__ == "__main__":
    # Simulated 4-byte masked WebSocket frame sent from a client browser
    mock_websocket_packet = bytes([
        0x81,  # FIN bit set, Opcode 1 (Text Frame representation)
        0x84,  # Mask bit active, Payload length of 4 bytes
        0x1A, 0x2B, 0x3C, 0x4D,  # 4-Byte Client Mask Key
        0x72, 0x4E, 0x5D, 0x29   # Obfuscated payload content bytes for "saad"
    ])
    
    op, message = WebSocketFramer.decode_client_frame(mock_websocket_packet)
    print(f"Decoded Opcode Type Flag: {op} | Transmitted Cleartext Content: '{message}'")