"""
System: Ultra-High-Performance Space-Optimized Binary Time-Series Datastore
Description: A high-efficiency metric storage engine that compresses multi-sensor metrics 
             into aligned binary streams using zero-allocation memory slices.
Lead Engineer: Syed Saad Bin Irfan
"""

import os
import struct
import time
import logging
from typing import Dict, List, Tuple, Any, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Binary-Store) %(message)s')

class TimeSeriesMetricRecord:
    """Represents an immutable, structured snapshot record tracking hardware metric properties."""
    __slots__ = ("timestamp", "sensor_id", "core_utilization", "temperature_kelvin")
    
    def __init__(self, timestamp: int, sensor_id: int, core_utilization: float, temperature_kelvin: float) -> None:
        self.timestamp: int = timestamp
        self.sensor_id: int = sensor_id
        self.core_utilization: float = core_utilization
        self.temperature_kelvin: float = temperature_kelvin


class HighPerformanceBinaryDatastore:
    """Manages dense metrics storage files, packing structured data into optimized binary formats."""
    # Structural Layout: uint64 (Epoch), uint32 (Sensor ID), float (CPU usage), float (Temp)
    # Binary Footprint Map: 8 + 4 + 4 + 4 = 20 Bytes flat per data record block
    RECORD_STRUCT_FORMAT = "!QIff"
    RECORD_SIZE_BYTES = struct.calcsize(RECORD_STRUCT_FORMAT)

    def __init__(self, target_datastore_filepath: str) -> None:
        self.filepath: str = target_datastore_filepath
        logging.info(f"Binary storage engine active. Target data record boundary: {self.RECORD_SIZE_BYTES} bytes.")

    def append_metric_record(self, record: TimeSeriesMetricRecord) -> None:
        """Packs and writes metric data blocks straight into the binary storage file."""
        packed_binary_chunk = struct.pack(
            self.RECORD_STRUCT_FORMAT,
            record.timestamp,
            record.sensor_id,
            self.core_utilization, # Using mapped class object parameters
            record.temperature_kelvin
        )
        
        with open(self.filepath, "ab") as store_file:
            store_file.write(packed_binary_chunk)

    def query_metrics_range_zero_allocation(self, start_epoch: int, end_epoch: int) -> List[TimeSeriesMetricRecord]:
        """Queries metric ranges from the file block using zero-allocation sliding memory views."""
        matched_records_list: List[TimeSeriesMetricRecord] = []
        
        if not os.path.exists(self.filepath):
            return matched_records_list

        # Read the file contents entirely into a single byte array partition block
        with open(self.filepath, "rb") as src_file:
            raw_binary_blob = src_file.read()

        total_bytes_length = len(raw_binary_blob)
        # Wrap raw bytes in a zero-copy memoryview mask layer to parse elements quickly
        shared_memory_view = memoryview(raw_binary_blob)
        current_byte_offset = 0

        while current_byte_offset + self.RECORD_SIZE_BYTES <= total_bytes_length:
            # Unpack attributes directly from the current memory coordinates without creating sub-array copies
            record_attributes_tuple = struct.unpack_from(
                self.RECORD_STRUCT_FORMAT, 
                shared_memory_view, 
                current_byte_offset
            )
            
            timestamp, sensor_id, core_util, temp_k = record_attributes_tuple
            
            # Filter entries cleanly using target timestamp range criteria
            if start_epoch <= timestamp <= end_epoch:
                matched_records_list.append(
                    TimeSeriesMetricRecord(timestamp, sensor_id, core_util, temp_k)
                )
                
            current_byte_offset += self.RECORD_SIZE_BYTES

        return matched_records_list


if __name__ == "__main__":
    print("\n=== SYSTEM START: HIGH PERFORMANCE BINARY TIME-SERIES DATASTORE ===\n")
    target_store = "system_telemetry_matrix.bin"
    
    engine = HighPerformanceBinaryDatastore(target_store)
    base_epoch_time = int(time.time())

    # Instantiate the data object metrics tracking array
    metric_one = TimeSeriesMetricRecord(base_epoch_time - 10, 1001, 0.421, 302.5)
    metric_two = TimeSeriesMetricRecord(base_epoch_time - 5, 1002, 0.895, 312.8)
    metric_three = TimeSeriesMetricRecord(base_epoch_time, 1001, 0.512, 304.2)

    logging.info("Committing metric records directly into space-optimized binary storage layout...")
    engine.append_metric_record(metric_one)
    engine.append_metric_record(metric_two)
    engine.append_metric_record(metric_three)

    # Query metrics from a targeted time window
    logging.info("Executing zero-allocation range queries over the data file blocks...")
    results = engine.query_metrics_range_zero_allocation(base_epoch_time - 8, base_epoch_time + 1)

    print(f"\nQuery Extraction Output Summary:\n{'-'*50}")
    print(f"Total matching elements discovered: {len(results)}")
    for idx, item in enumerate(results, start=1):
        print(f" Record #{idx} -> Epoch: {item.timestamp} | Sensor ID: {item.sensor_id} | CPU: {item.core_utilization:.2%}")
    print("-" * 50)

    # Clean up workspace file artifacts
    if os.path.exists(target_store):
        os.remove(target_store)