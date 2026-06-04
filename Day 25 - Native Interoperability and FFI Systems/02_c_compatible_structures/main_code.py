"""
Core Topic: C-Compatible Struct Packing and Data Modeling
Description: Models hardware-aligned contiguous C structures directly inside Python memory maps.
Lead Engineer: Syed Saad Bin Irfan
"""

import ctypes

class NetworkPacketHeader(ctypes.Structure):
    """Defines a contiguous, hardware-aligned binary structural layout mapping straight to C definitions."""
    # Maps directly to standard structural components using native C types signatures
    _fields_ = [
        ("packet_id", ctypes.c_uint32),
        ("flags_bitmap", ctypes.c_uint8),
        ("payload_length", ctypes.c_uint16),
        ("transmission_latency", ctypes.c_double)
    ]

class StructuredPayloadSerializer:
    """Handles parsing and extraction operations across C-compatible structure memory blocks."""
    @staticmethod
    def inspect_structure_properties(packet_instance: NetworkPacketHeader) -> dict:
        return {
            "Total Memory Footprint Bytes": ctypes.sizeof(packet_instance),
            "Packet ID Offset Bytes": NetworkPacketHeader.packet_id.offset,
            "Flags Bitmap Offset Bytes": NetworkPacketHeader.flags_bitmap.offset,
            "Payload Length Offset Bytes": NetworkPacketHeader.payload_length.offset,
            "Latency Offset Bytes": NetworkPacketHeader.transmission_latency.offset,
        }

if __name__ == "__main__":
    # Create an active packet structure instance in memory
    packet = NetworkPacketHeader(
        packet_id=99214, 
        flags_bitmap=0b00001011, 
        payload_length=512, 
        transmission_latency=0.00421
    )

    print("[C-STRUCT] Structure initialized. Inspecting low-level memory byte alignment offsets:")
    metadata = StructuredPayloadSerializer.inspect_structure_properties(packet)
    for key, val in metadata.items():
        print(f"  {key}: {val}")

    # Proving memory modifications occur instantly on fields
    packet.packet_id = 100001
    print(f"[C-STRUCT] Mutation update validation. New Packet ID: {packet.packet_id}")