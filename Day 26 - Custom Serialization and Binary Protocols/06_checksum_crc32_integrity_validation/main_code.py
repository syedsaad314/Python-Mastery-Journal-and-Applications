"""
Core Topic: Cyclic Redundancy Check (CRC32) Data Integrity Verification
Description: Calculates bitwise validation hashes to catch packet corruption across transmission lines.
Lead Engineer: Syed Saad Bin Irfan
"""

import binascii

class DataIntegrityVerifier:
    """Computes and validates CRC32 check codes to secure data transfers against corruption."""
    
    @staticmethod
    def generate_crc32_signature(data_bytes: bytes) -> int:
        """Calculates a 32-bit cyclical redundancy verification hash over a byte payload."""
        # Bitwise masking ensures returned hashes map consistently to unsigned 32-bit boundaries
        return binascii.crc32(data_bytes) & 0xFFFFFFFF

    @classmethod
    def secure_packet_frame(cls, raw_payload_bytes: bytes) -> bytes:
        """Appends an automated 4-byte verification hash tail to secure a data payload."""
        crc_checksum = cls.generate_crc32_signature(raw_payload_bytes)
        # Pack the 32-bit hash into a 4-byte network big-endian suffix tail
        crc_suffix_tail = struct.pack("!I", crc_checksum)
        return raw_payload_bytes + crc_suffix_tail

    @classmethod
    def verify_and_strip_packet(cls, protected_packet_bytes: bytes) -> bytes:
        """Validates payload codes, throwing anomalies if data corruption is detected."""
        if len(protected_packet_bytes) < 4:
            raise ValueError("Packet payload length cannot breach minimum 4-byte check caps.")
            
        payload_body = protected_packet_bytes[:-4]
        transmitted_crc_hash, = struct.unpack("!I", protected_packet_bytes[-4:])
        
        computed_crc_hash = cls.generate_crc32_signature(payload_body)
        
        if computed_crc_hash != transmitted_crc_hash:
            raise ConnectionAbortedError("Data corruption anomaly detected! CRC signature verification match failed.")
            
        return payload_body


if __name__ == "__main__":
    import struct
    print("[INTEGRITY-CHECK] Starting packet hash verification runs...")
    
    clean_data = b"CRITICAL_CLUSTER_STATE_PARAMETER"
    secured_wire_packet = DataIntegrityVerifier.secure_packet_frame(clean_data)
    
    unpacked_payload = DataIntegrityVerifier.verify_and_strip_packet(secured_wire_packet)
    print(f"[INTEGRITY-CHECK] Verification matched successfully. Payload extracted: '{unpacked_payload.decode()}'")

    try:
        # Simulate an in-transit bit flip corruption error
        corrupted_packet_bytes = bytearray(secured_wire_packet)
        corrupted_packet_bytes[2] ^= 0b00100000  # Flip a data bit
        
        DataIntegrityVerifier.verify_and_strip_packet(bytes(corrupted_packet_bytes))
    except ConnectionAbortedError:
        print("[INTEGRITY-CHECK] Data integrity guard worked perfectly. Corrupted packet intercepted and dropped.")