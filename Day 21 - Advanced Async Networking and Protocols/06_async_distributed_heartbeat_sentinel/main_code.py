"""
Core Topic: Network Keep-Alive Heartbeat Sentinel
Description: Verifies node health by parsing inbound token payloads over TCP sockets.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio

class DistributedHeartbeatSentinel:
    def __init__(self, expected_token: str = "HEARTBEAT_PING") -> None:
        self.token: str = expected_token
        self.last_heartbeat_received: float = 0.0

    async def evaluate_heartbeat_stream(self, raw_data_bytes: bytes) -> bool:
        """Validates incoming token bytes to verify node health status."""
        try:
            decoded_string = raw_data_bytes.decode('utf-8').strip()
            if decoded_string == self.token:
                self.last_heartbeat_received = asyncio.get_running_loop().time()
                print(f"[SENTINEL] Valid token received at metric tick: {self.last_heartbeat_received:.2f}")
                return True
            print(f"[SENTINEL] Invalid token string payload matched: '{decoded_string}'")
            return False
        except UnicodeDecodeError:
            return False

async def main() -> None:
    sentinel = DistributedHeartbeatSentinel()
    # Test validation rules against correct and malformed byte sequences
    assert await sentinel.evaluate_heartbeat_stream(b"HEARTBEAT_PING\n") == True
    assert await sentinel.evaluate_heartbeat_stream(b"CORRUPT_TOKEN_DATA\n") == False
    print("[SENTINEL] All automated packet verification checks validated successfully.")

if __name__ == "__main__":
    asyncio.run(main())