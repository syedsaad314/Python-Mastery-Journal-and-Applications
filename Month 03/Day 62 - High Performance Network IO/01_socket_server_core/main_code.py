# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Non-Blocking TCP Socket Server Core
Description: Initializes a low-level, non-blocking TCP listener using raw sockets 
             to handle network event loops without thread pool depletion.
"""
import socket

class NonBlockingServerCore:
    def __init__(self, host: str = "127.0.0.1", port: int = 9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def configure_interface(self) -> None:
        # Allow instant address reuse to prevent TCP TIME_WAIT locks
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(128)
        # Shift execution layer out of blocking behavior into event management
        self.server_socket.setblocking(False)

    def accept_inbound_connection(self) -> tuple[socket.socket, tuple[str, int]] | None:
        try:
            client_socket, address = self.server_socket.accept()
            client_socket.setblocking(False)
            return client_socket, address
        except BlockingIOError:
            # Re-routed: System resources are clear, but no pending sync events exist
            return None

if __name__ == "__main__":
    server = NonBlockingServerCore()
    server.configure_interface()
    # Execute a clean polling test run to verify structural initialization
    result = server.accept_inbound_connection()
    assert result is None
    print(f"[TASK 01 PASSED] Non-blocking socket listener bounded to {server.host}:{server.port}")