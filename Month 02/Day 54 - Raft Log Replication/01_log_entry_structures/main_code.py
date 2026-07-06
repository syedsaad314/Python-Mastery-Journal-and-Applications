# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Log Entry Structural Schemas
Description: Implements the fundamental entry primitives carrying term data, 
             position values, and command instructions.
"""
from typing import NamedTuple, Any

class LogEntry(NamedTuple):
    term: int
    index: int
    command: Any

class LogBuffer:
    def __init__(self) -> None:
        self.entries: list[LogEntry] = []

    def append_entry(self, term: int, command: Any) -> int:
        next_index = len(self.entries) + 1
        entry = LogEntry(term=term, index=next_index, command=command)
        self.entries.append(entry)
        return next_index

if __name__ == "__main__":
    buffer = LogBuffer()
    idx = buffer.append_entry(term=1, command={"op": "SET", "key": "a", "val": 100})
    assert idx == 1
    assert buffer.entries[0].index == 1