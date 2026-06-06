"""
Core Topic: Edge-Triggered vs Level-Triggered Notification Modes
Description: Implements full socket draining loops to manage edge-triggered network events.
Lead Engineer: Syed Saad Bin Irfan
"""

import socket
import errno
from typing import List

class EdgeTriggeredIoDrainer:
    """Drains non-blocking socket streams completely to prevent event starvation in edge-triggered modes."""
    
    @staticmethod
    def drain_socket_payload_completely(client_sock: socket.socket) -> bytes:
        """Drains the socket's internal OS buffers completely until an EAGAIN block occurs."""
        accumulated_payload = bytearray()
        client_sock.setblocking(False)
        
        while True:
            try:
                chunk = client_sock.recv(4) # Intentionally small chunk size to simulate loop iterations
                if not chunk:
                    # Connection closed cleanly by remote endpoint
                    break
                accumulated_payload.extend(chunk)
            except OSError as exc:
                if exc.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                    # Buffers drained completely; safe to exit loop
                    break
                raise exc
                
        return bytes(accumulated_payload)


if __name__ == "__main__":
    print("[IO-DRAINER] Initiating Edge-Triggered verification run execution stubs...")
    
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 9906))
    listener.listen(1)

    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect(("127.0.0.1", 9906))
    receiver, _ = listener.accept()

    sender.sendall(b"DENSE_EDGE_TRIGGERED_STREAM_DATA_METRIC")
    sender.close()

    result_bytes = EdgeTriggeredIoDrainer.drain_socket_payload_completely(receiver)
    print(f"[IO-DRAINER] Complete structural payload drained safely: {result_bytes.decode()}")
    
    receiver.close()
    listener.close()