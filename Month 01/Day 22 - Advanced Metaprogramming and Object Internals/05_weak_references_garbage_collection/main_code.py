"""
Core Topic: Weak References and Garbage Collection Lifecycle Hooks
Description: Bypasses memory lock states using weakref links to let transient objects evaporate cleanly.
Lead Engineer: Syed Saad Bin Irfan
"""

import gc
import weakref

class EphemeralTelemetryNode:
    """A data tracking node class that executes cleanups automatically upon deletion."""
    def __init__(self, node_id: str) -> None:
        self.id: str = node_id

    def __del__(self) -> None:
        print(f"[MEMORY KERNEL] Node reference '{self.id}' dropped from memory context.")


if __name__ == "__main__":
    # Instantiate a transient cache resource object
    target_node = EphemeralTelemetryNode("TRANSIENT-CACHE-01")
    
    # Establish a weak reference link that does not increment the object's internal reference counter
    weak_pointer = weakref.ref(target_node)
    
    print(f"[WEAKREF] Pointer target resolution: {weak_pointer()}")
    
    print("[WEAKREF] Severing primary strong reference object anchor...")
    del target_node  # Triggers automatic cleanup immediately because weak references do not block garbage collection
    
    # Force an immediate garbage collection sweep
    gc.collect()
    
    print(f"[WEAKREF] Evaluation post-deletion: {weak_pointer()}")