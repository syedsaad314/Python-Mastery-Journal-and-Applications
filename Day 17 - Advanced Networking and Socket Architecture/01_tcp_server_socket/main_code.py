"""
Core Topic: Low-Level TCP Socket Architecture
Description: Instantiates a primitive stream socket listener handling explicit byte buffer streams.
Lead Engineer: Syed Saad Bin Irfan
"""

import socket

class TCPServerSocket:
    def __init__(self, host: str = "127.0.0.1", port: int = 8085) -> None:
        self.host: str = host
        self.port: int = port
        self.server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow instant address reuse to eliminate OS timeout holding states
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_listening(self) -> None:
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[TCP SERVER] Actively accepting socket streams on {self.host}:{self.port}")

        try:
            while True:
                client_sock, client_addr = self.server_socket.accept()
                print(f"[TCP SERVER] Inbound socket connection secured from: {client_addr}")
                
                # Fetch bytes safely through a fixed 1024-byte chunk frame window
                raw_payload = client_sock.recv(1024)
                if raw_payload:
                    decoded_msg = raw_payload.decode('utf-8').strip()
                    print(f"[TCP SERVER] Inbound Payload: {decoded_msg}")
                    
                    # Echo acknowledgment packet back across the established connection path
                    client_sock.sendall(b"PACKET_RECEIVED\n")
                client_sock.close()
        except KeyboardInterrupt:
            print("\n[TCP SERVER] Shutting down connection interface channels safely.")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    # Designed for testing via command line: 'curl http://127.0.0.1:8085' or netcat
    server = TCPServerSocket()
    # To run without blocking scripts indefinitely during generation:
    # server.start_listening()