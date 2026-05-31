"""
System: High-Throughput Async Log Ingestion TCP Server
Description: A high-performance TCP server that ingests concurrent socket log streams, 
             routes records via async queues, and implements clean shutdown controls.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import json
import logging
import sys
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Parser Node) %(message)s')

class AsyncLogIngestionServer:
    def __init__(self, binding_host: str = "127.0.0.1", operational_port: int = 8888) -> None:
        self.host: str = binding_host
        self.port: int = operational_port
        self.log_ingestion_queue: asyncio.Queue = asyncio.Queue(maxsize=50)
        self.server_instance: Optional[asyncio.AbstractServer] = None # type: ignore
        self.processed_records_cache: List[Dict[str, Any]] = []
        self.is_running: bool = True

    async def _parse_log_worker_routine(self) -> None:
        """Processes incoming raw log strings from the queue, sanitizing and writing records to memory storage."""
        while self.is_running or not self.log_ingestion_queue.empty():
            try:
                # Use a timeout to keep the loop active during low-traffic periods
                raw_log_line = await asyncio.wait_for(self.log_ingestion_queue.get(), timeout=1.0)
                
                logging.info(f"[WORKER] Parsing incoming raw log string payload...")
                # Extract and clean structured log entries
                sanitized_log = raw_log_line.strip().decode('utf-8', errors='ignore')
                
                # Apply data transformations to raw metrics
                enriched_record = {
                    "raw_message": sanitized_log,
                    "ingestion_timestamp": asyncio.get_running_loop().time(),
                    "length_bytes": len(sanitized_log)
                }
                
                self.processed_records_cache.append(enriched_record)
                self.log_ingestion_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as internal_err:
                logging.error(f"[WORKER ERROR] Data processing fault encountered: {internal_err}")

    async def _handle_inbound_connection_stream(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handles active client connections and reads data streams line-by-line until EOF."""
        client_address = writer.get_extra_info('peername')
        logging.info(f"[SERVER] Accepted inbound stream connection from client: {client_address}")

        try:
            while True:
                # Read arriving stream segments line-by-line asynchronously
                data_bytes = await reader.readline()
                if not data_bytes:  # Stream terminated by client
                    break
                
                # Push data into the processing queue; yield execution if the queue is full
                await self.log_ingestion_queue.put(data_bytes)
                logging.info(f"[SERVER] Stream buffer enqueued ({len(data_bytes)} bytes) from client {client_address}.")
                
                # Send a quick confirmation back down the network connection socket
                writer.write(b"ACK_STREAM_RECEIVED\n")
                await writer.drain()

        except Exception as stream_err:
            logging.error(f"[SERVER ERROR] Stream connection dropped for client {client_address}: {stream_err}")
        finally:
            logging.info(f"[SERVER] Closing stream connection socket for client: {client_address}")
            writer.close()
            await writer.wait_closed()

    async def boot_ingestion_engine(self) -> None:
        """Starts the log server and initializes background processing workers."""
        logging.info(f"Initializing TCP Ingestion Daemon on interface {self.host}:{self.port}...")
        
        # Start the background log processing worker task
        self.worker_task = asyncio.create_task(self._parse_log_worker_routine())
        
        # Bind the TCP stream server to the designated network port
        self.server_instance = await asyncio.start_server(
            self._handle_inbound_connection_stream, 
            self.host, 
            self.port
        )

        logging.info("TCP Server online. Awaiting data stream broadcasts...")
        async with self.server_instance:
            # Keep the server alive and listening for connections
            await self.server_instance.serve_forever()

    async def terminate_engine_gracefully(self) -> None:
        """Shuts down the server instance safely, ensuring all remaining queue items are processed."""
        logging.info("Shutdown signal caught. Commencing graceful teardown procedures...")
        self.is_running = False
        
        if self.server_instance:
            self.server_instance.close()
            await self.server_instance.wait_closed()
            logging.info("TCP Ingestion network listener closed down successfully.")

        # Wait for any remaining queue items to be fully cleared
        await self.log_ingestion_queue.join()
        await self.worker_task
        logging.info("All buffered log payloads flushed to memory cache storage.")

# Simulated Client Script to test the running ingestion server architecture
async def simulate_active_log_client() -> None:
    """Connects to the server, transfers test logs, and exits cleanly."""
    await asyncio.sleep(1.0) # Wait brief period for the server to finish initialization steps
    logging.info("[CLIENT TEST] Connecting to local ingestion engine...")
    
    try:
        reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
        
        mock_logs = [b"SYS_LOG::SYSTEM_BOOT_INIT\n", b"SYS_LOG::DB_POOL_OPENED_OK\n"]
        for log in mock_logs:
            logging.info(f"[CLIENT TEST] Broadcasting log data payload: {log.strip()}")
            writer.write(log)
            await writer.drain()
            
            response = await reader.readline()
            logging.info(f"[CLIENT TEST] Server confirmation received: {response.strip().decode()}")
            await asyncio.sleep(0.2)

        writer.close()
        await writer.wait_closed()
    except Exception as e:
        logging.error(f"[CLIENT TEST] Client execution aborted: {e}")

async def main_orchestration_scope() -> None:
    engine = AsyncLogIngestionServer()
    
    # Run the client simulation and server engine concurrently on the event loop
    server_task = asyncio.create_task(engine.boot_ingestion_engine())
    client_task = asyncio.create_task(simulate_active_log_client())

    await client_task
    await asyncio.sleep(0.5) # Allow background processes time to finish parsing raw lines
    
    # Trigger a graceful shutdown sequence on the engine context
    await engine.terminate_engine_gracefully()
    server_task.cancel() # Break the infinite loop block on serve_forever() safely

    print(f"\n=== CAPTURED LOG RECORDS STORAGE LOGS ===\n")
    print(json.dumps(engine.processed_records_cache, indent=4))

if __name__ == "__main__":
    asyncio.run(main_orchestration_scope())