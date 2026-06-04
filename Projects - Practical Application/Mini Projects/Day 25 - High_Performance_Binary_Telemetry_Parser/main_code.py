"""
System: Zero-Serialization High-Performance Binary Telemetry Ingestion Parser
Description: An ultra-fast, zero-copy binary parser that overrides serialization layers 
             by mapping network byte frames directly onto memory-aligned C structures.
Lead Engineer: Syed Saad Bin Irfan
"""

import ctypes
import logging
import sys
import time
from typing import Dict, Any, List, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Telemetry-Ingest) %(message)s')

class TelemetryDataPayload(ctypes.Structure):
    """Defines a strict, hardware-aligned binary structure layout matching uncompressed sensor frame packages."""
    _pack_ = 1  # Force strict 1-byte structural alignment packing, eliminating compiler-injected padding bytes
    _fields_ = [
        ("sensor_node_id", ctypes.c_uint32),   # 4 Bytes
        ("operational_mode", ctypes.c_uint8),  # 1 Byte
        ("reading_metric_count", ctypes.c_uint16), # 2 Bytes
        ("core_temperature", ctypes.c_float),  # 4 Bytes
        ("voltage_reading", ctypes.c_double)   # 8 Bytes -> Total Size: 19 bytes packed strictly
    ]


class FastTelemetryParserEngine:
    """High-speed stream processor that extracts binary telemetry frames via zero-copy data views."""
    def __init__(self) -> None:
        self.frame_capacity = ctypes.sizeof(TelemetryDataPayload)
        logging.info(f"Telemetry parsing engine ready. Fixed frame size boundary allocation: {self.frame_capacity} bytes.")

    def ingest_raw_stream_frame(self, raw_buffer_bytes: bytes) -> Tuple[bool, Optional[Dict[str, Any]]]: # type: ignore
        """Maps raw byte sequences straight onto memory structures without instantiating high-level parse trees."""
        if len(raw_buffer_bytes) != self.frame_capacity:
            logging.error(f"Ingestion rejected: Buffer size length mismatch. Expected {self.frame_capacity}, got {len(raw_buffer_bytes)}.")
            return False, None

        # Create a zero-copy, readable view directly over the incoming byte buffer array
        native_struct_view = TelemetryDataPayload.from_buffer_copy(raw_buffer_bytes)

        # Extract values directly from memory fields
        extracted_metadata = {
            "node_identity_id": native_struct_view.sensor_node_id,
            "mode_bitmap": hex(native_struct_view.operational_mode),
            "total_metrics_logged": native_struct_view.reading_metric_count,
            "temperature_celsius": round(native_struct_view.core_temperature, 2),
            "voltage_level_volts": round(native_struct_view.voltage_reading, 4)
        }
        return True, extracted_metadata


if __name__ == "__main__":
    print("\n=== SYSTEM START: HIGH PERFORMANCE ZERO-COPY TELEMETRY PARSER ===\n")
    parser = FastTelemetryParserEngine()

    # Synthesize a raw, compressed binary byte frame stream payload to simulate arriving network traffic
    # Layout format: uint32 (202611), uint8 (0x0B), uint16 (128), float (42.85), double (5.0024)
    # Binary Signature Layout: 4 bytes + 1 byte + 2 bytes + 4 bytes + 8 bytes = 19 bytes total
    import struct
    simulated_wire_bytes = struct.pack("<IBHfd", 202611, 0x0B, 128, 42.85, 5.0024)
    
    logging.info(f"Simulated wire frame metrics generated. Length: {len(simulated_wire_bytes)} bytes.")

    start_timestamp = time.perf_counter()
    success, metrics_packet = parser.ingest_raw_stream_frame(simulated_wire_bytes)
    duration_sec = time.perf_counter() - start_timestamp

    if success and metrics_packet:
        logging.info(f"Parsing pass complete in {duration_sec * 1000000:.2f} microseconds.")
        print(f"\nExtracted Telemetry Metadata Packet Details:\n{'-'*45}")
        for key, value in metrics_packet.items():
            print(f"  {key:<25} : {value}")
        print("-" * 45)