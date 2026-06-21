"""
Core Topic: Consumer Group Partition Rebalancing
Description: Dynamically allocates topic partitions among active group consumers.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class ConsumerGroupCoordinator:
    """Coordinates partition assignment logic across active consumer threads."""
    
    def __init__(self, total_partitions: int) -> None:
        self.total_partitions = total_partitions
        self.active_consumers: List[str] = []

    def register_consumer(self, consumer_id: str) -> Dict[str, List[int]]:
        """Registers a new consumer instance and triggers a partition rebalance cycle."""
        if consumer_id not in self.active_consumers:
            self.active_consumers.append(consumer_id)
        return self.trigger_rebalance()

    def trigger_rebalance(self) -> Dict[str, List[int]]:
        """Distributes partition assignments evenly across all active consumers."""
        assignments: Dict[str, List[int]] = {c: [] for c in self.active_consumers}
        if not self.active_consumers:
            return assignments

        for partition_idx in range(self.total_partitions):
            # Apply round-robin distribution mapping
            consumer_pos = partition_idx % len(self.active_consumers)
            target_consumer = self.active_consumers[consumer_pos]
            assignments[target_consumer].append(partition_idx)

        print(f"[REBALANCE] Distributed {self.total_partitions} partitions across {len(self.active_consumers)} active consumers.")
        return assignments


if __name__ == "__main__":
    coordinator = ConsumerGroupCoordinator(total_partitions=4)
    
    # Simulate single consumer claiming all partitions
    print("State 1:", coordinator.register_consumer("worker-A"))
    # Simulate scale-out event causing partition reassignment
    print("State 2:", coordinator.register_consumer("worker-B"))