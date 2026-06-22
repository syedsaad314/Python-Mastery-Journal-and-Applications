"""
Core Topic: Zero-Copy String and Array Slicing via Memoryviews
Description: Intercepts and parses sliding packet frames without duplicating underlying buffer variables.
Lead Engineer: Syed Saad Bin Irfan
"""

import time

class ZeroCopySlicingEngine:
    """Demonstrates how to slice and manipulate data blocks cleanly without copying byte arrays."""
    @staticmethod
    def extract_checksum_region_zero_copy(raw_payload_bytes: bytearray) -> memoryview:
        """Generates a slice pointer view targeting explicit byte coordinates directly."""
        # memoryview wraps data references without triggering high-overhead array copy operations
        master_view = memoryview(raw_payload_bytes)
        # Isolate coordinates 4 through 8 via standard sliding array indices
        return master_view[4:8]


if __name__ == "__main__":
    print("[ZERO-COPY] Initializing memoryview performance verification sweeps...")
    
    # Establish a sample shared data array block
    shared_data_stream = bytearray(b"HEADER_PACKET_TOKEN_SIGNATURE_DATA_STREAM")
    
    slice_pointer = ZeroCopySlicingEngine.extract_checksum_region_zero_copy(shared_data_stream)
    print(f"[ZERO-COPY] Extracted slice window contents: {slice_pointer.tobytes().decode()}")

    # Modify data values directly inside the slice pointer view
    # This alters the parent data array instantly because both point to identical memory addresses
    slice_pointer[0:4] = b"ZONE"
    
    print(f"[ZERO-COPY] Parent stream post-mutation check: {shared_data_stream}")
    assert shared_data_stream.startswith(b"HEADZONE_PAC")