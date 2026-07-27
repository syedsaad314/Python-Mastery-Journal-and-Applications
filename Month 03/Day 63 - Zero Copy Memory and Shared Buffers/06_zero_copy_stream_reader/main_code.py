# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Zero-Copy Network Ingestion Engine via socket.recv_into
Description: Ingests network packet streams directly into pre-allocated memory slices 
             using socket.recv_into(), bypassing intermediate network allocation layers.
"""
import socket

class ZeroCopyStreamIngestor:
    @staticmethod
    def execute_direct_socket_ingest() -> bytes:
        # Setup socket pair to simulate direct kernel-to-memory stream ingestion
        server_soc, client_soc = socket.socketpair()
        
        try:
            client_soc.sendall(b"NETWORK_PACKET_DIRECT_INJECT_PAYLOAD")
            
            # Pre-allocate buffer and slice memoryview to target exact destination region
            preallocated_buffer = bytearray(64)
            view_slice = memoryview(preallocated_buffer)[0:36]
            
            # Direct socket stream copy straight into memory slice
            bytes_received = server_soc.recv_into(view_slice)
            return bytes(preallocated_buffer[:bytes_received])
            
        finally:
            server_soc.close()
            client_soc.close()

if __name__ == "__main__":
    received_bytes = ZeroCopyStreamIngestor.execute_direct_socket_ingest()
    assert received_bytes == b"NETWORK_PACKET_DIRECT_INJECT_PAYLOAD"
    print(f"[TASK 06 PASSED] Ingested {len(received_bytes)} bytes directly into target pre-allocated RAM slice.")