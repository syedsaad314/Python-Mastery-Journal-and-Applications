"""
Core Topic: Zero-Allocation I/O Buffering via socket.recv_into
Description: Minimizes garbage collection churn by reading network bytes straight into reusable memory arrays.
Lead Engineer: Syed Saad Bin Irfan
"""

import socket
import os

class ZeroAllocationIoEngine:
    """Executes high-throughput network streaming operations using pre-allocated memory slices."""
    
    def __init__(self, allocation_size_bytes: int = 1024) -> None:
        # Pre-allocate a single reusable bytearray buffer in RAM memory space
        self._shared_buffer = bytearray(allocation_size_bytes)
        # Wrap the byte array in a zero-copy memoryview mask layer
        self.memory_view = memoryview(self._shared_buffer)

    def process_incoming_stream(self, client_sock: socket.socket) -> int:
        """Reads stream bytes directly into the reusable memory view, avoiding temporary string copies."""
        # Read incoming data straight into our pre-allocated memory coordinates
        bytes_extracted = client_sock.recv_into(self.memory_view, 1024)
        return bytes_extracted

    def extract_working_slice(self, length: int) -> bytes:
        """Exposes the active data window slice without duplicating the underlying buffer."""
        return self.memory_view[:length].tobytes()


if __name__ == "__main__":
    engine = ZeroAllocationIoEngine(512)
    print(f"[ZERO-ALLOC-IO] Memory view block initialized. Internal buffer address: {id(engine._shared_buffer)}")
    
    # Establish a local communication pair to test streaming operations
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 9905))
    listener.listen(1)

    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect(("127.0.0.1", 9905))
    receiver, _ = listener.accept()

    sender.sendall(b"ZERO_ALLOCATION_METRIC_FRAME")
    
    bytes_read = engine.process_incoming_stream(receiver)
    extracted_data = engine.extract_working_slice(bytes_read)
    
    print(f"[ZERO-ALLOC-IO] Extracted {bytes_read} bytes payload: {extracted_data}")
    
    # Clean up open resources
    sender.close()
    receiver.close()
    listener.close()