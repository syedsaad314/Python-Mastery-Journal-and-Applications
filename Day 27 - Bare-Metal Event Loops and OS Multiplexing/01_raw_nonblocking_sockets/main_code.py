"""
Core Topic: Raw Non-Blocking Sockets and Non-Blocking Error Trapping
Description: Configures primitive TCP sockets to execute asynchronously without blocking threads.
Lead Engineer: Syed Saad Bin Irfan
"""

import socket
import errno
import time

class NonBlockingSocketListener:
    """Manages low-level non-blocking server socket handshakes and error handling loops."""
    
    @staticmethod
    def initialize_server(host: str = "127.0.0.1", port: int = 9901) -> socket.socket:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Shift socket operations straight into non-blocking execution mode
        server_sock.setblocking(False)
        server_sock.bind((host, port))
        server_sock.listen(5)
        return server_sock

    @classmethod
    def poll_connections(cls, server_sock: socket.socket, duration_seconds: float = 2.0) -> None:
        """Polls for incoming connections via non-blocking error interception hooks."""
        print("[SOCKET-NB] Non-blocking accept loop running. Polling for connections...")
        end_time = time.time() + duration_seconds
        
        while time.time() < end_time:
            try:
                client_sock, client_addr = server_sock.accept()
                print(f"[SOCKET-NB] Success! Inbound connection established from: {client_addr}")
                client_sock.close()
            except OSError as exc:
                # Intercept expected non-blocking resource starvation indicators
                if exc.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                    # Kernel has no pending connections inside the sync back-log array
                    time.sleep(0.1)
                    continue
                raise exc


if __name__ == "__main__":
    server = NonBlockingSocketListener.initialize_server()
    try:
        NonBlockingSocketListener.poll_connections(server, duration_seconds=1.0)
    finally:
        server.close()
        print("[SOCKET-NB] Context teardown complete.")