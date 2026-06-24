# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Memory State Serialization
Description: Converts active volatile runtime dictionaries into immutable, structured byte footprints.
"""
import json
from typing import Dict

class StateSerializer:
    @staticmethod
    def serialize_runtime_memory(memory_state: Dict[str, str]) -> bytes:
        # Enforce canonical sorted keys layout to guarantee reproducible checksum hashes
        json_str = json.dumps(memory_state, sort_keys=True, separators=(',', ':'))
        return json_str.encode('utf-8')

if __name__ == "__main__":
    active_memory = {"user": "saad", "role": "admin", "status": "active"}
    serialized_bytes = StateSerializer.serialize_runtime_memory(active_memory)
    
    assert isinstance(serialized_bytes, bytes)
    assert serialized_bytes == b'{"role":"admin","status":"active","user":"saad"}'