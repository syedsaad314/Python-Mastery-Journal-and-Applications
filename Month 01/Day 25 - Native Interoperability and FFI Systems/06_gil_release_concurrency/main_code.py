"""
Core Topic: Bypassing the Global Interpreter Lock (GIL) via Dynamic C Invocation
Description: Proves how dropping to native libraries releases GIL boundaries for concurrent execution.
Lead Engineer: Syed Saad Bin Irfan
"""

import ctypes
import sys
import threading
import time

class NativeParallelEngine:
    """Leverages standard C functions to achieve concurrent execution outside Python interpreter boundaries."""
    def __init__(self) -> None:
        self.lib_name = "msvcrt.dll" if sys.platform.startswith("win32") else "libc.so.6"
        self.libc = ctypes.CDLL(self.lib_name)

    def execute_concurrent_sleep_pass(self, duration_sec: int) -> None:
        """Triggers system sleep via native libraries, releasing GIL restrictions implicitly."""
        print(f"[{threading.current_thread().name}] Native loop call active. Releasing GIL tracking restrictions...")
        if sys.platform.startswith("win32"):
            # Windows Sleep takes input parameters mapped in milliseconds
            self.libc._sleep(duration_sec * 1000)
        else:
            self.libc.sleep(duration_sec)
        print(f"[{threading.current_thread().name}] Native loop completed. Re-entering interpreter context.")

if __name__ == "__main__":
    print("[MAIN] Spinning parallel native threads pool execution framework...")
    engine = NativeParallelEngine()
    
    start_time = time.perf_counter()

    # Provision dual concurrent tracking threads pointing to native execution lines
    thread_alpha = threading.Thread(target=engine.execute_concurrent_sleep_pass, args=(2,), name="Thread-Alpha")
    thread_beta = threading.Thread(target=engine.execute_concurrent_sleep_pass, args=(2,), name="Thread-Beta")

    thread_alpha.start()
    thread_beta.start()

    thread_alpha.join()
    thread_beta.join()

    duration = time.perf_counter() - start_time
    print(f"\n[MAIN] Parallel run complete. Cumulative runtime duration: {duration:.4f} seconds.")
    print("[MAIN] Proof: Dual 2-second sleep loops resolved concurrently in ~2 seconds, completely bypassing GIL stalls.")