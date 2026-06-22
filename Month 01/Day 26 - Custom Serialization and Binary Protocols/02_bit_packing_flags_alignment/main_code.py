"""
Core Topic: Low-Level Bitwise Property Compaction
Description: Compresses multiple boolean flags and enum states into a single byte field.
Lead Engineer: Syed Saad Bin Irfan
"""

class SystemStateFramer:
    """Packs and unpacks discrete multi-property statuses into single-byte configurations."""
    # Define exact bit shifting masks for individual state variables
    MASK_ENGINE_ACTIVE = 1 << 0  # Bit index 0
    MASK_ERROR_TRIGGERED = 1 << 1  # Bit index 1
    MASK_SSL_CONNECTED   = 1 << 2  # Bit index 2
    # Node Role uses bits 3 and 4 to store values from 0 to 3 (2-bit range capacity)
    SHIFT_NODE_ROLE      = 3
    MASK_NODE_ROLE       = 0b11 << SHIFT_NODE_ROLE

    @classmethod
    def pack_flags(cls, active: bool, error: bool, ssl: bool, role_id: int) -> int:
        """Packs individual parameters into a highly optimized single-byte layout."""
        packed_byte = 0
        if active: packed_byte |= cls.MASK_ENGINE_ACTIVE
        if error:  packed_byte |= cls.MASK_ERROR_TRIGGERED
        if ssl:    packed_byte |= cls.MASK_SSL_CONNECTED
        
        # Clamp user parameter values to a 2-bit range to prevent bit-bleeding accidents
        sanitized_role = role_id & 0x03
        packed_byte |= (sanitized_role << cls.SHIFT_NODE_ROLE)
        return packed_byte

    @classmethod
    def unpack_flags(cls, packed_byte: int) -> dict:
        """Extracts status variables back out from a single-byte container using bitwise masking."""
        return {
            "engine_active": (packed_byte & cls.MASK_ENGINE_ACTIVE) != 0,
            "error_triggered": (packed_byte & cls.MASK_ERROR_TRIGGERED) != 0,
            "ssl_connected": (packed_byte & cls.MASK_SSL_CONNECTED) != 0,
            "node_role_id": (packed_byte & cls.MASK_NODE_ROLE) >> cls.SHIFT_NODE_ROLE
        }


if __name__ == "__main__":
    print("[BIT-PACKING] Initiating structural state compression verification passes...")
    
    # Pack four independent variables into a single byte block
    compiled_byte = SystemStateFramer.pack_flags(active=True, error=False, ssl=True, role_id=2)
    print(f"[BIT-PACKING] Resulting structural state element output: {bin(compiled_byte)} ({compiled_byte} raw value)")
    
    extracted_map = SystemStateFramer.unpack_flags(compiled_byte)
    print(f"[BIT-PACKING] Extraction matrix components returned: {extracted_map}")
    
    assert extracted_map["engine_active"] is True
    assert extracted_map["node_role_id"] == 2