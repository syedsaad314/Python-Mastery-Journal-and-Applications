"""
System: Ultra-Low Latency Zero-Copy Matrix Stream Processing Pipeline
Description: A high-performance IPC processing system that streams numeric matrices across 
             isolated processes using zero-copy raw memory maps and atomic event gates.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
from multiprocessing import shared_memory
import ctypes
import logging
import time

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (IPC-Matrix-Pipeline) %(message)s')

class LowLatencyMatrixStream:
    """Allocates a high-performance shared memory channel for moving matrix arrays without serialization copy blocks."""
    def __init__(self, rows: int = 4, cols: int = 4, channel_name: str = "shared_matrix_stream_channel") -> None:
        self.rows = rows
        self.cols = cols
        self.total_elements = rows * cols
        # Calculate size based on 64-bit floating point structures (8 bytes per item)
        self.element_size = ctypes.sizeof(ctypes.c_double)
        self.total_bytes = self.total_elements * self.element_size
        self.channel_name = channel_name
        
        # Instantiate synchronization gates to manage access timing across processes
        self.data_ready_gate = multiprocessing.Event()
        self.processing_done_gate = multiprocessing.Event()

    def create_master_allocation_context(self) -> shared_memory.SharedMemory:
        """Allocates the primary shared memory segment block from the operating system kernel."""
        return shared_memory.SharedMemory(name=self.channel_name, create=True, size=self.total_bytes)

    def bind_to_existing_context(self) -> shared_memory.SharedMemory:
        """Binds a separate child worker process to the pre-existing shared memory block."""
        return shared_memory.SharedMemory(name=self.channel_name)


def matrix_producer_process(stream_manager: LowLatencyMatrixStream) -> None:
    """Generates continuous matrix telemetry data frames directly into the shared memory segment."""
    logging.info("Producer process started. Binding to shared memory frame...")
    shm = stream_manager.bind_to_existing_context()
    
    # Cast raw memory bytes to an accessible double precision array pointer structure
    matrix_array_view = (ctypes.c_double * stream_manager.total_elements).from_buffer(shm.buf)
    
    logging.info("Generating and writing matrix data directly into shared RAM...")
    for index in range(stream_manager.total_elements):
        # Generate dummy data simulation calculations (e.g., identity configurations)
        matrix_array_view[index] = float(index * 1.5)
        
    # Dispatch an atomic synchronization signal to alert consumer processes
    stream_manager.data_ready_gate.set()
    
    # Block until the consumer finishes processing modifications
    logging.info("Producer waiting for consumer pipeline confirmation...")
    stream_manager.processing_done_gate.wait()
    
    shm.close()
    logging.info("Producer detached from shared segment safely.")


def matrix_consumer_transform_process(stream_manager: LowLatencyMatrixStream) -> None:
    """Intercepts raw shared matrix data arrays to apply low-level value transformations."""
    logging.info("Consumer transform process started. Waiting for data availability signal...")
    stream_manager.data_ready_gate.wait()
    
    shm = stream_manager.bind_to_existing_context()
    matrix_array_view = (ctypes.c_double * stream_manager.total_elements).from_buffer(shm.buf)
    
    logging.info("Applying matrix transformations directly in-place on shared memory...")
    for index in range(stream_manager.total_elements):
        # Apply an in-place math scale calculation directly onto the shared memory view
        matrix_array_view[index] = matrix_array_view[index] * 2.0
        
    shm.close()
    logging.info("Consumer transformation task complete. Dropping gate triggers.")
    stream_manager.processing_done_gate.set()


if __name__ == "__main__":
    print("\n=== SYSTEM START: ZERO COPY IPC MATRIX PIPELINE ===\n")
    pipeline = LowLatencyMatrixStream()
    
    # Allocate the primary memory block before spinning up workers
    master_shm = pipeline.create_master_allocation_context()
    
    # Setup worker processes
    producer = multiprocessing.Process(target=matrix_producer_process, args=(pipeline,))
    consumer = multiprocessing.Process(target=matrix_consumer_transform_process, args=(pipeline,))
    
    consumer.start()
    producer.start()
    
    producer.join()
    consumer.join()
    
    # Verify the in-place transformations directly from the master memory pointer
    final_view = (ctypes.c_double * pipeline.total_elements).from_buffer(master_shm.buf)
    print("\n[VERIFICATION] Final Transformed Matrix Extracted from Master Memory Node:")
    
    for r in range(pipeline.rows):
        row_values = [final_view[r * pipeline.cols + c] for c in range(pipeline.cols)]
        print(f"  Row {r}: {row_values}")
        
    master_shm.close()
    master_shm.unlink()
    print("\n=== SYSTEM SHUTDOWN: ZERO COPY IPC MATRIX PIPELINE CLEAN ===")