"""
Component: Multi-Threaded Consumer Group
Description: Manages background consumer loops that poll and process partitioned event logs.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
import threading
from typing import List, Dict
from message_broker import CentralMessageBroker

class DistributedStreamConsumer:
    """Spawns background polling worker threads to process events from assigned partitions."""
    
    def __init__(self, group_id: str, worker_id: str, broker: CentralMessageBroker) -> None:
        self.group_id = group_id
        self.worker_id = worker_id
        self.broker = broker
        self.assigned_partitions: List[int] = []
        self.processed_event_count = 0
        self.is_running = False
        self._thread: Optional[threading.Thread] = None # type: ignore

    def start_polling_loop(self) -> None:
        self.is_running = True
        self._thread = threading.Thread(target=self._poll_broker_partitions, daemon=True)
        self._thread.start()

    def _poll_broker_partitions(self) -> None:
        """Continuously loops through and processes events from assigned partitions."""
        while self.is_running:
            if not self.assigned_partitions:
                time.sleep(0.2)
                continue

            for p_id in list(self.assigned_partitions):
                # Fetch last committed checkpoint offset index
                current_offset = self.broker.get_committed_offset(self.group_id, p_id)
                records = self.broker.partitions[p_id].read_from_offset(current_offset)

                for msg in records:
                    # Emulate business logic processing
                    time.sleep(0.1) 
                    self.processed_event_count += 1
                    # Commit next sequential tracking checkpoint offset coordinate
                    self.broker.commit_consumer_offset(self.group_id, p_id, msg["offset"] + 1)

            time.sleep(0.2) # Throttles polling frequency to avoid burning CPU cycles

    def stop(self) -> None:
        self.is_running = False