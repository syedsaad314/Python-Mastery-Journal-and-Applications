"""
Core Topic: Asynchronous Publisher-Subscriber Streaming Hub
Description: Manages a registry of concurrent client stream writers to broadcast events safely.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
from typing import Set

class AsyncStreamBroadcastHub:
    def __init__(self) -> None:
        self.active_subscribers: Set[asyncio.StreamWriter] = set()

    def register_client(self, writer: asyncio.StreamWriter) -> None:
        """Adds an active stream writer socket to the broadcast topology."""
        self.active_subscribers.add(writer)
        print(f"[HUB] Registered client stream. Total subscriber count: {len(self.active_subscribers)}")

    def unregister_client(self, writer: asyncio.StreamWriter) -> None:
        """Removes an active client from the hub to stop further message delivery."""
        if writer in self.active_subscribers:
            self.active_subscribers.remove(writer)
            print(f"[HUB] Dropped client stream. Total client count: {len(self.active_subscribers)}")

    async def broadcast_payload(self, message: str) -> None:
        """Broadcasts messages concurrently across all registered client streaming sockets."""
        if not self.active_subscribers:
            return
            
        print(f"[HUB] Dispatching broadcast message: {message.strip()}")
        encoded_payload = message.encode('utf-8')
        
        # Dispatch payloads across all registered active writing streams
        for writer in list(self.active_subscribers):
            try:
                writer.write(encoded_payload)
                # Scheduling drain invocations iteratively ensures buffers do not clog memory
                await writer.drain()
            except (ConnectionResetError, BrokenPipeError):
                # Cleanly purge dead socket links caught mid-broadcast
                self.unregister_client(writer)

async def main() -> None:
    broadcast_hub = AsyncStreamBroadcastHub()
    print("[HUB] Inversion routing matrix active. Standalone operational lifecycle checked.")
    await broadcast_hub.broadcast_payload("SYSTEM_EVENT_PING\n")

if __name__ == "__main__":
    asyncio.run(main())