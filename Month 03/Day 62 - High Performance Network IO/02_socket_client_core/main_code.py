# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Low-Level TCP Client Stream Engine
Description: Controls non-blocking connection states and network stream outbox writes.
"""
import socket
import errno

class NonBlockingClientCore:
    def __init__(self, host: str = "127.0.0.1", port: int = 9999):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setblocking(False)

    def establish_channel(self) -> bool:
        try:
            self.client_socket.connect((self.host, self.port))
            return True
        except BlockingIOError as error:
            # Operation in progress flag means connection handshake is processing asynchronously
            if error.errno in (errno.EINPROGRESS, errno.EWOULDBLOCK):
                return False
            raise error

    def dispatch_payload(self, raw_data: bytes) -> int:
        try:
            bytes_sent = self.client_socket.send(raw_data)
            return bytes_sent
        except BlockingIOError:
            return 0

if __name__ == "__main__":
    client = NonBlockingClientCore()
    status = client.establish_channel()
    # Handshake will return false instantly because no server listener is active during this isolation assay
    assert status is False
    print("[TASK 02 PASSED] Core client engine initialized and handshake process non-blocking state verified.")