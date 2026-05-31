"""
Core Topic: Low-Level Duplex Pipe Communication
Description: Establishes a synchronized point-to-point connection utilizing multiprocessing.Pipe.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
import os
from typing import Tuple

def pipe_endpoint_worker(connection_handle: multiprocessing.connection.Connection) -> None:
    """Consumes an arbitrary packet string and returns a synchronized binary acknowledgment confirmation."""
    try:
        # Await inbound data payload across the channel pipe frame
        inbound_packet = connection_handle.recv()
        print(f"[CHILD PID: {os.getpid()}] Received inbound payload: {inbound_packet}")
        
        # Transform data and transmit responses back down the reverse duplex line path
        transformed_payload = f"PROCESSED_SUCCESSFULLY::{inbound_packet}"
        connection_handle.send(transformed_payload)
    finally:
        connection_handle.close()

if __name__ == "__main__":
    # Pipe returns a duplex (two-way) connection channel tuple pair
    parent_conn, child_conn = multiprocessing.Pipe(duplex=True)
    
    worker = multiprocessing.Process(target=pipe_endpoint_worker, args=(child_conn,))
    worker.start()
    
    outbound_msg = "TRANSACTION_ID_99214_EXEC"
    print(f"[PARENT PID: {os.getpid()}] Dispatching data wire payload: {outbound_msg}")
    parent_conn.send(outbound_msg)
    
    # Block and wait for response data back from the wire endpoint channel link
    response = parent_conn.recv()
    print(f"[PARENT PID: {os.getpid()}] Received pipeline confirmation: {response}")
    
    worker.join()
    parent_conn.close()