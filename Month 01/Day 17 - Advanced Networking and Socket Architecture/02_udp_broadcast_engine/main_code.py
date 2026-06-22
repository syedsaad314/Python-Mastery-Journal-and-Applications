"""
Core Topic: Connectionless UDP Broadcast Transmission
Description: Configures a datagram transmitter leveraging socket-level broadcast properties.
Lead Engineer: Syed Saad Bin Irfan
"""

import socket
import time

class UDPBroadcastEngine:
    def __init__(self, broadcast_port: int = 9005) -> None:
        self.port: int = broadcast_port
        # SOCK_DGRAM instantiates a connectionless UDP interface
        self.tx_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Configure the socket level options to grant explicit broadcast broadcast privileges
        self.tx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def emit_beacon(self, status_payload: str) -> None:
        """Transmits an un-targeted network datagram broadcast to all subnet interfaces."""
        broadcast_destination = ("255.255.255.255", self.port)
        encoded_payload = status_payload.encode('utf-8')
        
        self.tx_socket.sendto(encoded_payload, broadcast_destination)
        print(f"[UDP BROADCAST] Fired beacon packet out to sub-net grid on port {self.port}")

    def close_engine(self) -> None:
        self.tx_socket.close()

if __name__ == "__main__":
    engine = UDPBroadcastEngine()
    engine.emit_beacon("CLUSTER_NODE_SAAD_ACTIVE")
    engine.close_engine()