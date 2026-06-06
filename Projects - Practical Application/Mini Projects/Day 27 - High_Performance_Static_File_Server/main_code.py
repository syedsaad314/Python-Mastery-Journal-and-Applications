"""
System: High-Performance Single-Threaded Asynchronous Static File Server
Description: Serves file chunks asynchronously without blocking execution threads, leveraging custom multiplexing selectors.
Lead Engineer: Syed Saad Bin Irfan
"""

import socket
import selectors
import os
import logging
from typing import Dict, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Async-FileServer) %(message)s')

class AsyncStaticFileServer:
    """An event-driven file server that handles concurrent connections on a single execution thread."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 9081) -> None:
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()
        # Maps client sockets directly to their active file transfer status trackers
        self.active_transfers: Dict[socket.socket, Tuple[int, int, Any]] = {} # type: ignore

    def boot_server(self) -> None:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.setblocking(False)
        server_sock.bind((self.host, self.port))
        server_sock.listen(128)
        
        self.selector.register(server_sock, selectors.EVENT_READ, data=self._accept_connection)
        logging.info(f"File Server active and listening on interface: http://{self.host}:{self.port}")

    def _accept_connection(self, server_sock: socket.socket, mask: int) -> None:
        client_sock, addr = server_sock.accept()
        client_sock.setblocking(False)
        logging.info(f"New client socket route established from: {addr}")
        
        # Register the client socket to monitor for incoming HTTP requests
        self.selector.register(client_sock, selectors.EVENT_READ, data=self._read_http_request)

    def _read_http_request(self, client_sock: socket.socket, mask: int) -> None:
        try:
            request_bytes = client_sock.recv(1024)
            if not request_bytes:
                self._terminate_client_session(client_sock)
                return

            # Open a sample local metric report file to demonstrate file streaming
            mock_filename = "ubit_performance_report.txt"
            if not os.path.exists(mock_filename):
                with open(mock_filename, "w") as f:
                    f.write("DCS-UBIT CAMPUS LOG COMPILATION MATRIX TRACKS\n" * 50)

            file_descriptor = open(mock_filename, "rb")
            file_size = os.path.getsize(mock_filename)
            
            # Send initial HTTP headers down the wire
            http_header = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Length: {file_size}\r\n"
                "Content-Type: text/plain\r\n\r\n"
            )
            client_sock.sendall(http_header.encode('utf-8'))
            
            # Update the event registration to monitor when the socket is ready for writes
            self.selector.modify(client_sock, selectors.EVENT_WRITE, data=self._pump_file_chunks)
            self.active_transfers[client_sock] = (file_descriptor, file_size, 0)
            
        except Exception as err:
            logging.error(f"Error encountered parsing client HTTP lines: {err}")
            self._terminate_client_session(client_sock)

    def _pump_file_chunks(self, client_sock: socket.socket, mask: int) -> None:
        file_desc, total_size, total_bytes_sent = self.active_transfers[client_sock]
        
        try:
            # Read a chunk from the file and push it down the socket pipeline
            file_desc.seek(total_bytes_sent)
            chunk = file_desc.read(4096)
            
            if chunk:
                bytes_sent = client_sock.send(chunk)
                new_sent_total = total_bytes_sent + bytes_sent
                self.active_transfers[client_sock] = (file_desc, total_size, new_sent_total)
                
                if new_sent_total < total_size:
                    return # Continue streaming in subsequent event loop iterations

            # File transfer completed successfully; close open descriptors
            logging.info("Static payload file transfer completed successfully.")
            file_desc.close()
            self._terminate_client_session(client_sock)
            
        except OSError as exc:
            import errno
            if exc.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                return
            self._terminate_client_session(client_sock)

    def _terminate_client_session(self, client_sock: socket.socket) -> None:
        if client_sock in self.active_transfers:
            file_desc, _, _ = self.active_transfers[client_sock]
            try:
                file_desc.close()
            except Exception: pass
            del self.active_transfers[client_sock]
            
        try:
            self.selector.unregister(client_sock)
            client_sock.close()
        except Exception: pass

    def run_event_loop(self, cycles: int = 5) -> None:
        for _ in range(cycles):
            events = self.selector.select(timeout=0.2)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


if __name__ == "__main__":
    server_instance = AsyncStaticFileServer()
    server_instance.boot_server()
    try:
        server_instance.run_event_loop(cycles=3)
    finally:
        # Cleanup mock file artifacts
        if os.path.exists("ubit_performance_report.txt"):
            os.remove("ubit_performance_report.txt")
        print("[SERVER] Shutdown sequence complete.")