"""
Core Topic: OS Selector Event Multiplexing (epoll / kqueue)
Description: Multiplexes single-threaded I/O operations across multiple sockets via selectors.
Lead Engineer: Syed Saad Bin Irfan
"""

import socket
import selectors
from typing import List, Tuple

class KernelMultiplexReactor:
    """Orchestrates multi-socket monitoring paths leveraging default OS polling selectors."""
    
    def __init__(self) -> None:
        # Automatically select the best kernel mechanism available (epoll, kqueue, select)
        self.selector = selectors.DefaultSelector()
        self.server_sockets: List[socket.socket] = []

    def bind_listener(self, host: str, port: int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)
        sock.bind((host, port))
        sock.listen(128)
        
        # Register the socket with the OS selector to monitor for incoming read events
        self.selector.register(sock, selectors.EVENT_READ, data=self._accept_handler)
        self.server_sockets.append(sock)
        print(f"[SELECTOR] Monitoring interface bound to port: {port}")

    def _accept_handler(self, key_obj: selectors.SelectorKey) -> None:
        server_sock = key_obj.fileobj
        client_sock, addr = server_sock.accept()
        print(f"[SELECTOR] Connection routed cleanly from: {addr}")
        client_sock.close()

    def step_event_loop(self) -> None:
        """Executes a single event-loop step, blocking only until the kernel detects I/O."""
        events = self.selector.select(timeout=0.5)
        for key, mask in events:
            callback_procedure = key.data
            callback_procedure(key)

    def close(self) -> None:
        for sock in self.server_sockets:
            self.selector.unregister(sock)
            sock.close()
        self.selector.close()


if __name__ == "__main__":
    reactor = KernelMultiplexReactor()
    reactor.bind_listener("127.0.0.1", 9902)
    try:
        # Run a brief event loop step execution test
        reactor.step_event_loop()
    finally:
        reactor.close()