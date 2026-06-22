"""
Core Topic: Non-Blocking I/O Multiplexing
Description: Manages multiple network connection states on a single thread using the selectors module.
Lead Engineer: Syed Saad Bin Irfan
"""

import selectors
import socket
from typing import Any

class SocketMultiplexer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8090) -> None:
        self.host: str = host
        self.port: int = port
        self.selector: selectors.DefaultSelector = selectors.DefaultSelector()
        
    def _accept_connection_callback(self, server_sock: socket.socket) -> None:
        """Accepts an incoming connection from the listening socket and registers it with the selector."""
        client_sock, client_addr = server_sock.accept()
        print(f"[MULTIPLEXER] Accepting client socket connection link from: {client_addr}")
        client_sock.setblocking(False)
        
        # Register the client socket for read-ready events
        self.selector.register(client_sock, selectors.EVENT_READ, data=self._read_connection_callback)

    def _read_connection_callback(self, client_sock: socket.socket) -> None:
        """Reads incoming data from a client socket when it has bytes ready for consumption."""
        try:
            data_bytes = client_sock.recv(1024)
            if data_bytes:
                print(f"[MULTIPLEXER] Consumed stream data chunk: {data_bytes.decode('utf-8').strip()}")
                client_sock.sendall(b"MULTIPLEX_ACK\n")
            else:
                # No data means the client dropped the socket connection link
                print("[MULTIPLEXER] Connection closed by remote client endpoint.")
                self.selector.unregister(client_sock)
                client_sock.close()
        except ConnectionResetError:
            self.selector.unregister(client_sock)
            client_sock.close()

    def run_event_loop(self) -> None:
        """Starts the multiplexer loop, listening for incoming network events."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        server_socket.setblocking(False)
        
        # Register the main listening socket for connection-ready events
        self.selector.register(server_socket, selectors.EVENT_READ, data=self._accept_connection_callback)
        print(f"[MULTIPLEXER] Core Event loop listening on {self.host}:{self.port}...")

        try:
            # Run for a brief test window or loop indefinitely
            for _ in range(3):
                events = self.selector.select(timeout=1.0)
                for key, mask in events:
                    callback_fn = key.data
                    callback_fn(key.fileobj)
        finally:
            self.selector.close()

if __name__ == "__main__":
    multiplexer_node = SocketMultiplexer()
    multiplexer_node.run_event_loop()