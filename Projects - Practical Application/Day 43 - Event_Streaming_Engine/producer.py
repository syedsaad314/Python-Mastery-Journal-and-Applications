"""
Component: Idempotent Event Producer
Description: Handles event partitioning mechanics and ensures idempotent message write delivery.
Lead Engineer: Syed Saad Bin Irfan
"""

import json
import hashlib
from typing import Dict, tuple
from message_broker import CentralMessageBroker

class IdempotentEventProducer:
    """Ingests data streams, applies routing rules, and guarantees duplicate-free message delivery."""
    
    def __init__(self, producer_id: str, broker_reference: CentralMessageBroker) -> None:
        self.producer_id = producer_id
        self.broker = broker_reference
        self.sequence_counter = 0

    def broadcast_event(self, routing_key: str, event_type: str, data: Dict[str, any]) -> tuple[int, int]:
        """Partitions messages via hashing and delivers them idempotently with sequence checking numbers."""
        # Calculate target partition by hashing the routing key to distribute the load evenly
        hash_digest = hashlib.md5(routing_key.encode('utf-8')).hexdigest()
        target_partition_id = int(hash_digest, 16) % len(self.broker.partitions)

        payload_packet = {
            "producer_id": self.producer_id,
            "sequence_number": self.sequence_counter,
            "routing_key": routing_key,
            "event_type": event_type,
            "body": data
        }

        # Deliver message and get its committed log offset index
        offset = self.broker.publish_to_partition(target_partition_id, payload_packet)
        self.sequence_counter += 1
        return target_partition_id, offset