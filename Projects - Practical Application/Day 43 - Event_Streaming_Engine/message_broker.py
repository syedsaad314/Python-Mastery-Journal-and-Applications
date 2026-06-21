"""
Component: Message Broker Engine
Description: Manages multi-partition topics, append-only logs, and thread-safe consumer offset tracking.
Lead Engineer: Syed Saad Bin Irfan
"""

import threading
from typing import Dict, List, Optional

class TopicPartition:
    """Represents an isolated partition log inside a specific message stream topic."""
    
    def __init__(self, partition_id: int) -> None:
        self.partition_id = partition_id
        self.log: List[Dict[str, any]] = []
        self._lock = threading.Lock()

    def append(self, message: Dict[str, any]) -> int:
        with self._lock:
            offset = len(self.log)
            message["offset"] = offset
            self.log.append(message)
            return offset

    def read_from_offset(self, start_offset: int) -> List[Dict[str, any]]:
        with self._lock:
            if start_offset < len(self.log):
                return self.log[start_offset:]
            return []


class CentralMessageBroker:
    """Coordinates horizontally scaled topic streams and tracks committed consumer offsets."""
    
    def __init__(self, topic_name: str, total_partitions: int = 3) -> None:
        self.topic_name = topic_name
        self.partitions: Dict[int, TopicPartition] = {
            i: TopicPartition(i) for i in range(total_partitions)
        }
        self.offset_registry: Dict[str, Dict[int, int]] = {}
        self._registry_lock = threading.Lock()

    def publish_to_partition(self, partition_id: int, message: Dict[str, any]) -> int:
        """Routes an incoming event message directly to its designated partition log."""
        if partition_id in self.partitions:
            return self.partitions[partition_id].append(message)
        raise ValueError("Invalid target partition coordinate.")

    def commit_consumer_offset(self, group_id: str, partition_id: int, offset: int) -> None:
        """Safely commits processing progress checkpoints for a consumer group."""
        with self._registry_lock:
            if group_id not in self.offset_registry:
                self.offset_registry[group_id] = {}
            self.offset_registry[group_id][partition_id] = offset

    def get_committed_offset(self, group_id: str, partition_id: int) -> int:
        with self._registry_lock:
            return self.offset_registry.get(group_id, {}).get(partition_id, 0)