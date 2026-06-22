"""
Core Topic: Thread-Local Storage Isolation
Description: Allocates isolated, thread-specific storage fields that are inaccessible to other threads.
Lead Engineer: Syed Saad Bin Irfan
"""

import threading
import time

class ContextStorageRegistry:
    def __init__(self) -> None:
        # Create a thread-local storage object
        self.local_context = threading.local()

    def execute_transaction_context(self, user_session_token: str) -> None:
        # Assign values directly to the thread-local instance attributes
        self.local_context.session_id = user_session_token
        time.sleep(0.1)
        # Verify that despite concurrency, context states remain completely isolated
        print(f"[THREAD {threading.current_thread().name}] Session Isolated Token ID: {self.local_context.session_id}")

if __name__ == "__main__":
    registry = ContextStorageRegistry()
    
    t1 = threading.Thread(target=registry.execute_transaction_context, args=("TOKEN_SAAD_99",), name="Worker-Alpha")
    t2 = threading.Thread(target=registry.execute_transaction_context, args=("TOKEN_FABHA_88",), name="Worker-Beta")

    t1.start()
    t2.start()
    t1.join()
    t2.join()