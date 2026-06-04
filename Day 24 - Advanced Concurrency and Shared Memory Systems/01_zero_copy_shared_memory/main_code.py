"""
Core Topic: Zero-Copy Shared Memory Allocations via OS Contexts
Description: Allocates raw memory structures accessible by isolated processes, using struct binary mapping.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
from multiprocessing import shared_memory
import struct
import time

class SharedMetricsBuffer:
    """Manages raw byte allocations across process boundaries using C-style packing layout definitions."""
    # Binary layout signature: 2 integers and 1 float (8 bytes + 8 bytes + 8 bytes = 24 bytes total)
    STRUCT_FORMAT = "qqd" 

    def __init__(self, name: str = "shared_telemetry_block", create_new: bool = True) -> None:
        self.buffer_size = struct.calcsize(self.STRUCT_FORMAT)
        if create_new:
            self.shm = shared_memory.SharedMemory(name=name, create=True, size=self.buffer_size)
        else:
            self.shm = shared_memory.SharedMemory(name=name)

    def write_metrics(self, request_count: int, failure_count: int, processing_latency: float) -> None:
        """Packs metrics directly into the raw shared memory byte track."""
        packed_bytes = struct.pack(self.STRUCT_FORMAT, request_count, failure_count, processing_latency)
        self.shm.buf[:self.buffer_size] = packed_bytes

    def read_metrics(self) -> tuple:
        """Unpacks raw memory directly into an active Python tuple structure without object replication."""
        return struct.unpack(self.STRUCT_FORMAT, self.shm.buf[:self.buffer_size])

    def close_and_unlink(self) -> None:
        """Releases the memory mapping context safely back to the operating system."""
        self.shm.close()
        try:
            self.shm.unlink()
            print("[SHARED-MEMORY] Unlinked and recycled memory allocation node safely.")
        except FileNotFoundError:
            pass

def writer_process_worker() -> None:
    """Independent child worker execution context writing to existing shared memory."""
    time.sleep(0.1) # Ensure parent establishes block coordinates first
    worker_mem = SharedMetricsBuffer(create_new=False)
    print("[CHILD-WORKER] Bound to shared block. Writing diagnostic metrics stream...")
    worker_mem.write_metrics(54021, 12, 0.0034)
    worker_mem.close_and_unlink()

if __name__ == "__main__":
    print("[PARENT] Initializing raw shared memory space...")
    parent_mem = SharedMetricsBuffer(create_new=True)
    parent_mem.write_metrics(0, 0, 0.0)

    worker = multiprocessing.Process(target=writer_process_worker)
    worker.start()
    worker.join()

    req, fail, latency = parent_mem.read_metrics()
    print(f"[PARENT] Intercepted shared state: Requests={req} | Failures={fail} | Latency={latency}s")
    parent_mem.close_and_unlink()