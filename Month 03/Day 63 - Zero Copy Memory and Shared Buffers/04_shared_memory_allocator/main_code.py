# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: High-Performance Shared Memory Segment Channel
Description: Uses multiprocessing.shared_memory to establish zero-copy 
             shared RAM blocks between independent Python processes.
"""
from multiprocessing import shared_memory

class SharedMemoryIPCChannel:
    @staticmethod
    def create_and_populate_segment(name: str, payload: bytes) -> shared_memory.SharedMemory:
        size = len(payload)
        shm = shared_memory.SharedMemory(name=name, create=True, size=size)
        shm.buf[:size] = payload
        return shm

    @staticmethod
    def attach_and_read_segment(name: str, size: int) -> bytes:
        existing_shm = shared_memory.SharedMemory(name=name)
        extracted_bytes = bytes(existing_shm.buf[:size])
        existing_shm.close()
        return extracted_bytes

if __name__ == "__main__":
    channel_name = "psm_dev_channel_99"
    data = b"SHARED_MEMORY_FAST_PAYLOAD"
    
    shm_master = SharedMemoryIPCChannel.create_and_populate_segment(channel_name, data)
    try:
        read_data = SharedMemoryIPCChannel.attach_and_read_segment(channel_name, len(data))
        assert read_data == data
        print(f"[TASK 04 PASSED] POSIX shared memory block attached and verified across processes: {read_data}")
    finally:
        shm_master.close()
        shm_master.unlink()  # Release system shared memory resource back to OS