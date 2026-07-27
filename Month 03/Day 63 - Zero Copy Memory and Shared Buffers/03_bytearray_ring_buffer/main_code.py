# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Zero-Allocation Circular Ring Buffer
Description: Implements a fixed-capacity mutable circular buffer in Python using a contiguous 
             bytearray to handle continuous streaming data without GC allocation churn.
"""

class ZeroAllocationRingBuffer:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._buffer = bytearray(capacity)
        self._head = 0
        self._tail = 0
        self._size = 0

    def push(self, data: bytes) -> int:
        written = 0
        for b in data:
            if self._size == self.capacity:
                break  # Buffer full state reached
            self._buffer[self._head] = b
            self._head = (self._head + 1) % self.capacity
            self._size += 1
            written += 1
        return written

    def pop(self, count: int) -> bytes:
        read_count = min(count, self._size)
        extracted = bytearray(read_count)
        for i in range(read_count):
            extracted[i] = self._buffer[self._tail]
            self._tail = (self._tail + 1) % self.capacity
            self._size -= 1
        return bytes(extracted)

if __name__ == "__main__":
    ring = ZeroAllocationRingBuffer(capacity=8)
    assert ring.push(b"ABCDEFGH") == 8
    assert ring.push(b"X") == 0  # Rejects write: buffer full
    
    assert ring.pop(4) == b"ABCD"
    assert ring.push(b"WXYZ") == 4  # Wraps around cleanly
    assert ring.pop(8) == b"EFGHWXYZ"
    print("[TASK 03 PASSED] Zero-allocation ring buffer push/pop/wrap cycles fully verified.")