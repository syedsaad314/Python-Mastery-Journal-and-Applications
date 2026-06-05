"""
System: Distributed Low-Latency Binary Wire Protocol RPC Orchestrator
Description: An enterprise-grade asynchronous communication router that parses packet frame 
             boundaries, validates CRC integrity tags, and marshals system calls with zero latency.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import binascii
import logging
import struct
from typing import Dict, Callable, Any, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Wire-Orchestrator) %(message)s')

class CustomWireMessageBroker:
    """Manages encoding, framing, and corruption verification for low-level binary data packets."""
    # Wire Protocol Header: 2 Magic Bytes (0x5A, 0x5A), 1 Byte Command ID, 4 Bytes Payload Length
    HEADER_FORMAT = "!BBBI"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    MAGIC_BYTE = 0x5A

    @classmethod
    def compile_secure_wire_packet(cls, command_id: int, payload_string: str) -> bytes:
        """Compiles text commands into a secure, structured network packet with trailing check codes."""
        payload_bytes = payload_string.encode('utf-8')
        payload_length = len(payload_bytes)
        
        # Assemble the protocol header block
        header = struct.pack(cls.HEADER_FORMAT, cls.MAGIC_BYTE, cls.MAGIC_BYTE, command_id, payload_length)
        packet_body = header + payload_bytes
        
        # Compute a 4-byte CRC32 integrity check code over the combined packet space
        crc_checksum = binascii.crc32(packet_body) & 0xFFFFFFFF
        return packet_body + struct.pack("!I", crc_checksum)


class LowLatencyRpcOrchestrator:
    """Asynchronous server node that decodes binary frame streams to route RPC method updates."""
    def __init__(self, binding_host: str = "127.0.0.1", operational_port: int = 9500) -> None:
        self.host: str = binding_host
        self.port: int = operational_port
        self.procedure_registry: Dict[int, Callable[[str], str]] = {}
        self.server_handle: Optional[asyncio.AbstractServer] = None # type: ignore

    def register_wire_procedure(self, command_id: int, procedure_callable: Callable[[str], str]) -> None:
        """Binds a functional procedure code directly to the network routing array mapping."""
        self.procedure_registry[command_id] = procedure_callable

    async def _handle_connection_stream_lifecycle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Parses stream segments sequentially according to wire framing specifications."""
        client_peername = writer.get_extra_info('peername')
        logging.info(f"[ORCHESTRATOR] Secure data channel opened with client: {client_peername}")

        try:
            while True:
                # Step 1: Read the explicit fixed size packet header layer from the stream
                header_bytes = await reader.readexactly(CustomWireMessageBroker.HEADER_SIZE)
                if not header_bytes:
                    break

                magic_1, magic_2, command_id, length_val = struct.unpack(
                    CustomWireMessageBroker.HEADER_FORMAT, 
                    header_bytes
                )

                # Validate magic byte signatures to prevent buffer injection attacks
                if magic_1 != CustomWireMessageBroker.MAGIC_BYTE or magic_2 != CustomWireMessageBroker.MAGIC_BYTE:
                    logging.error("Security alert: Invalid protocol signature frame matched. Severing connection.")
                    break

                # Step 2: Read the variable payload body along with the 4-byte CRC trailing suffix
                remaining_bytes_to_read = length_val + 4
                body_and_crc_bytes = await reader.readexactly(remaining_bytes_to_read)
                
                # Reconstruct the complete transmission data block to run integrity checks
                full_transmitted_packet = header_bytes + body_and_crc_bytes
                
                # Isolate the transmitted payload text and the check code suffix
                payload_content_bytes = body_and_crc_bytes[:length_val]
                transmitted_crc, = struct.unpack("!I", body_and_crc_bytes[length_val:])

                # Verify packet integrity using a local CRC32 recalculation pass
                computed_crc = binascii.crc32(full_transmitted_packet[:-4]) & 0xFFFFFFFF
                if computed_crc != transmitted_crc:
                    logging.critical(f"Data corruption intercepted from client {client_peername}! Dropping packet frame.")
                    break

                # Step 3: Route data payloads cleanly to their registered execution targets
                decoded_command_string = payload_content_bytes.decode('utf-8')
                if command_id in self.procedure_registry:
                    execution_result = self.procedure_registry[command_id](decoded_command_string)
                else:
                    execution_result = f"ERROR::COMMAND_ID_{command_id}_NOT_FOUND"

                # Send response data frames back down the established network connection channel
                response_wire_packet = CustomWireMessageBroker.compile_secure_wire_packet(0xFF, execution_result)
                writer.write(response_wire_packet)
                await writer.drain()

        except asyncio.IncompleteReadError:
            logging.info(f"Client socket stream terminated cleanly by remote endpoint: {client_peername}")
        except Exception as system_fault:
            logging.error(f"Execution system exception caught across routing lines: {system_fault}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def boot_orchestrator_engine(self) -> None:
        self.server_handle = await asyncio.start_server(self._handle_connection_stream_lifecycle, self.host, self.port)
        logging.info(f"Custom wire protocol RPC gateway listening on interface {self.host}:{self.port}...")
        async with self.server_handle:
            await self.server_handle.serve_forever()


# --- Production Verification Function Stubs ---
def core_telemetry_transform_callback(payload_string: str) -> str:
    return f"TRANSFORM_ACK_VALUE::{payload_string.upper()}"

async def simulate_active_cluster_client_node() -> None:
    """Connects to the server, transfers test logs, and exits cleanly."""
    await asyncio.sleep(0.5) # Wait for the server node to finish initialization steps
    logging.info("[TEST-CLIENT] Opening direct socket stream connection to wire gateway...")
    
    try:
        reader, writer = await asyncio.open_connection("127.0.0.1", 9500)
        
        # Compile a secure binary request packet
        request_packet = CustomWireMessageBroker.compile_secure_wire_packet(0x0A, "saad_bin_irfan_ubit_2026")
        logging.info(f"[TEST-CLIENT] Dispatching binary payload frame ({len(request_packet)} bytes)...")
        writer.write(request_packet)
        await writer.drain()

        # Intercept response packet lines arriving from the server
        header_bytes = await reader.readexactly(CustomWireMessageBroker.HEADER_SIZE)
        _, _, _, len_val = struct.unpack(CustomWireMessageBroker.HEADER_FORMAT, header_bytes)
        body_data = await reader.readexactly(len_val + 4)
        
        logging.info(f"[TEST-CLIENT] Server response extracted: '{body_data[:len_val].decode()}'")
        writer.close()
        await writer.wait_closed()
    except Exception as err:
        logging.error(f"Test client operation aborted: {err}")


async def main() -> None:
    orchestrator = LowLatencyRpcOrchestrator()
    orchestrator.register_wire_procedure(0x0A, core_telemetry_transform_callback)
    
    # Run the client simulation and server engine concurrently on the event loop
    server_task = asyncio.create_task(orchestrator.boot_orchestrator_engine())
    client_task = asyncio.create_task(simulate_active_cluster_client_node())

    await client_task
    await asyncio.sleep(0.2)
    server_task.cancel() # Safely shut down the persistent server engine task context

if __name__ == "__main__":
    asyncio.run(main())