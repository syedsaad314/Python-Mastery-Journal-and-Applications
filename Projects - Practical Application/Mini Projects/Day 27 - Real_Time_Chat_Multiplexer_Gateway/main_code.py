"""
System: Enterprise-Grade Real-Time Broadcast Chat Multiplexer Gateway
Description: A high-throughput non-blocking chat gateway that multiplexes message broadcasting across multiple connections.
Lead Engineer: Syed Saad Bin Irfan
"""

import socket
import selectors
import logging
from typing import Set

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Chat-Gateway) %(message)s')

class RealTimeChatGatewayMultiplexer:
    """Coordinates message broadcasting across concurrent clients using a non-blocking multiplexing core."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 9082) -> None:
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()
        self.connected_clients: Set[socket.socket] = set()

    def boot_gateway(self) -> None:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.setblocking(False)
        server_sock.bind((self.host, self.port))
        server_sock.listen(256)
        
        self.selector.register(server_sock, selectors.EVENT_READ, data=self._accept_client)
        logging.info(f"Chat Gateway Multiplexer online at: {self.host}:{self.port}")

    def _accept_client(self, server_sock: socket.socket, mask: int) -> None:
        client_sock, addr = server_sock.accept()
        client_sock.setblocking(False)
        logging.info(f"[GATEWAY] Connection accepted from remote interface: {addr}")
        
        self.selector.register(client_sock, selectors.EVENT_READ, data=self._read_client_message)
        self.connected_clients.add(client_sock)

    def _read_client_message(self, client_sock: socket.socket, mask: int) -> None:
        try:
            message_bytes = client_sock.recv(1024)
            if not message_bytes:
                self._disconnect_client(client_sock)
                return
                
            # Broadcast the incoming message out to all other connected client sockets
            self._broadcast_payload(message_bytes, originator_sock=client_sock)
            
        except Exception:
            self._disconnect_client(client_sock)

    def _broadcast_payload(self, payload: bytes, originator_sock: socket.socket) -> None:
        """Broadcasts messages to all connected client nodes, handling socket blocking states safely."""
        disconnected_targets: Set[socket.socket] = set()
        
        for client in self.connected_clients:
            if client is not originator_sock:
                try:
                    # Attempt a direct, non-blocking send down the wire
                    client.sendall(payload)
                except OSError as exc:
                    import errno
                    if exc.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                        # Transient buffer block encountered; skip in this iteration loop pass
                        continue
                    disconnected_targets.add(client)

        # Clean up tracking maps for any disconnected clients caught during the loop
        for dead_client in disconnected_targets:
            self._disconnect_client(dead_client)

    def _disconnect_client(self, client_sock: socket.socket) -> None:
        logging.info("[GATEWAY] Client node disconnected. Scrubbing tracking references.")
        if client_sock in self.connected_clients:
            self.connected_clients.remove(client_sock)
        try:
            self.selector.unregister(client_sock)
            client_sock.close()
        except Exception: pass

    def run_tick(self) -> None:
        events = self.selector.select(timeout=0.1)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == "__main__":
    gateway = RealTimeChatGatewayMultiplexer()
    gateway.boot_gateway()
    # Execute a clean execution slice tick check
    gateway.run_tick()