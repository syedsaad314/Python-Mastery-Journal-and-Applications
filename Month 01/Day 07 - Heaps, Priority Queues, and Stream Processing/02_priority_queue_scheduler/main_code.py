"""
Core Topic: Priority Queue OS Task Broker Implementation
Description: Using priority metadata tags to route asynchronous workloads.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import heapq
import time

class SystemTaskScheduler:
    def __init__(self):
        self.task_queue = []
        # Monotonically increasing sequence count to guarantee stable sorting on matching priorities
        self.sequence_counter = 0

    def register_task(self, task_name: str, priority_tier: int) -> None:
        """
        Enqueues tasks into the system backend. 
        A lower priority_tier number indicates a more critical task.
        """
        # Store tuple structure: (priority_tier, sequence_counter, task_name)
        heapq.heappush(self.task_queue, (priority_tier, self.sequence_counter, task_name))
        self.sequence_counter += 1

    def execute_next_task(self) -> str:
        """Extracts and returns the highest priority job currently pending in the schedule."""
        if not self.task_queue:
            return "No pending execution frames found."
        priority, sequence, configuration_name = heapq.heappop(self.task_queue)
        return f"Executing [{configuration_name}] assigned to Priority Tier ({priority})"

if __name__ == "__main__":
    broker = SystemTaskScheduler()
    
    # Ingesting jobs across varying priority values
    broker.register_task("render_ui_background", priority_tier=3)
    broker.register_task("kernel_panic_flush", priority_tier=0)
    broker.register_task("network_buffer_read", priority_tier=1)
    broker.register_task("garbage_collection_sweep", priority_tier=3)
    
    print(broker.execute_next_task())
    print(broker.execute_next_task())
    print(broker.execute_next_task())