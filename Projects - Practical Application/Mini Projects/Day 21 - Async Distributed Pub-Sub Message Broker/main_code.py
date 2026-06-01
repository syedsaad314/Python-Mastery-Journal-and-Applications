"""
System: Async Distributed Pub-Sub Message Broker
Description: A high-performance, single-threaded TCP message broker supporting topic subscriptions,
             concurrent message broadcasting, and clean client lifecycle state management.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import logging
from typing import Dict, Set, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Broker-Core) %(message)s')

class DistributedPubSubBroker:
    def __init__(self, host: str = "127.0.0.1", port: int = 9999) -> None:
        self.host: str = host
        self.port: int = port
        # Map topics to sets of active subscriber stream writers
        self.topic_routing_matrix: Dict[str, Set[asyncio.StreamWriter]] = {}
        self.server_instance: Optional[asyncio.AbstractServer] = None # type: ignore

    async def _dispatch_to_topic_subscribers(self, target_topic: str, raw_payload_bytes: bytes) -> None:
        """Broadcasts payload data to all active subscriber sockets registered to a topic."""
        if target_topic not in self.topic_routing_matrix or not self.topic_routing_matrix[target_topic]:
            return

        dead_subscribers: Set[asyncio.StreamWriter] = set()
        subscribers = self.topic_routing_matrix[target_topic]
        
        logging.info(f"Broadcasting event to {len(subscribers)} subscribers on topic [{target_topic}]")
        
        for client_writer in list(subscribers):
            try:
                client_writer.write(raw_payload_bytes)
                await client_writer.drain()
            except (ConnectionResetError, BrokenPipeError):
                dead_subscribers.add(client_writer)

        # Purge disconnected sockets from the registry
        for stale_writer in dead_subscribers:
            subscribers.remove(stale_writer)

    async def _handle_connection_lifecycle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Parses custom streaming protocol commands over active client socket connections."""
        client_peername = writer.get_extra_info('peername')
        logging.info(f"New client channel connected from endpoint: {client_peername}")
        
        # Track topics registered by this specific connection to handle cleanup on disconnect
        client_subscriptions: Set[str] = set()

        try:
            while True:
                data_line = await reader.readline()
                if not data_line: # Client closed connection
                    break
                
                try:
                    command_payload = data_line.decode('utf-8').strip()
                    if not command_payload:
                        continue
                        
                    # Protocol Syntax: SUB:<topic> or PUB:<topic>:<message>
                    protocol_segments = command_payload.split(":", 2)
                    action_verb = protocol_segments[0].upper()

                    if action_verb == "SUB" and len(protocol_segments) >= 2:
                        target_topic = protocol_segments[1].strip()
                        if target_topic not in self.topic_routing_matrix:
                            self.topic_routing_matrix[target_topic] = set()
                        
                        self.topic_routing_matrix[target_topic].add(writer)
                        client_subscriptions.add(target_topic)
                        writer.write(f"SUB_ACK::{target_topic}\n".encode('utf-8'))
                        await writer.drain()

                    elif action_verb == "PUB" and len(protocol_segments) == 3:
                        target_topic = protocol_segments[1].strip()
                        message_body = protocol_segments[2]
                        formatted_broadcast = f"EVENT::{target_topic}::{message_body}\n"
                        
                        await self._dispatch_to_topic_subscribers(target_topic, formatted_broadcast.encode('utf-8'))
                        writer.write(b"PUB_ACK\n")
                        await writer.drain()
                    else:
                        writer.write(b"ERROR::INVALID_PROTOCOL_SYNTAX\n")
                        await writer.drain()
                        
                except Exception as parse_err:
                    logging.error(f"Error parsing client command frame: {parse_err}")
                    writer.write(b"ERROR::INTERNAL_PARSING_FAULT\n")
                    await writer.drain()

        except Exception as socket_fault:
            logging.error(f"Socket connection exception on channel {client_peername}: {socket_fault}")
        finally:
            logging.info(f"Client disconnected. Cleaning up subscriptions for endpoint: {client_peername}")
            # Purge client connections from all topic registries upon exit
            for topic in client_subscriptions:
                if topic in self.topic_routing_matrix:
                    self.topic_routing_matrix[topic].discard(writer)
            writer.close()
            await writer.wait_closed()

    async def start_broker_service(self) -> None:
        """Starts the TCP streaming server engine."""
        self.server_instance = await asyncio.start_server(
            self._handle_connection_lifecycle, 
            self.host, 
            self.port
        )
        logging.info(f"Distributed Pub-Sub Broker online on interface {self.host}:{self.port}")
        async with self.server_instance:
            await self.server_instance.serve_forever()

# Simulated integration script to test the running broker architecture
async def simulate_pub_sub_network() -> None:
    """Simulates active pub-sub network operations over the broker server."""
    await asyncio.sleep(0.5) # Wait for the broker server to finish initialization steps
    logging.info("[TEST-SUITE] Connecting subscriber and publisher client nodes...")
    
    try:
        # Step 1: Initialize Subscriber Client node
        sub_reader, sub_writer = await asyncio.open_connection("127.0.0.1", 9999)
        sub_writer.write(b"SUB:fintech_transactions\n")
        await sub_writer.drain()
        logging.info(f"[SUB-CLIENT] Response received: {(await sub_reader.readline()).decode().strip()}")

        # Step 2: Initialize Publisher Client node
        pub_reader, pub_writer = await asyncio.open_connection("127.0.0.1", 9999)
        pub_writer.write(b"PUB:fintech_transactions:TX_9901_APPROVED\n")
        await pub_writer.drain()
        logging.info(f"[PUB-CLIENT] Response received: {(await pub_reader.readline()).decode().strip()}")

        # Step 3: Verify delivery on the subscriber channel
        broadcast_delivery = await sub_reader.readline()
        logging.info(f"[SUB-CLIENT] Broadcast message captured: {broadcast_delivery.decode().strip()}")

        # Cleanly disconnect sockets
        for writer in [sub_writer, pub_writer]:
            writer.close()
            await writer.wait_closed()
    except Exception as test_err:
        logging.error(f"Test suite execution failed: {test_err}")

async def main() -> None:
    broker = DistributedPubSubBroker()
    # Run the integration simulation alongside the core broker server
    broker_task = asyncio.create_task(broker.start_broker_service())
    client_simulation_task = asyncio.create_task(simulate_pub_sub_network())

    await client_simulation_task
    await asyncio.sleep(0.2)
    broker_task.cancel() # Shut down the persistent server instance gracefully

if __name__ == "__main__":
    asyncio.run(main())