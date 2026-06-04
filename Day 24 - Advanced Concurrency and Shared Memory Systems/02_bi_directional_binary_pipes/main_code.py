"""
Core Topic: Duplex Communication Channels via Binary Framing
Description: Establishes low-overhead, bidirectional process communication using raw duplex connections.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
import os

class DuplexMessagingNode:
    """Manages secure transactional command tracking over an operating system duplex connection pair."""
    def __init__(self, target_connection) -> None:
        self.connection = target_connection

    def dispatch_command(self, action_header: str, payload_body: str) -> None:
        """Pushes structured command boundaries onto the channel pipeline."""
        framed_string = f"{action_header}::{payload_body}\n"
        self.connection.send(framed_string)

    def read_command(self) -> tuple:
        """Blocks until a valid string data frame passes down the pipe connection layer."""
        raw_payload = self.connection.recv()
        segments = raw_payload.strip().split("::", 1)
        if len(segments) == 2:
            return segments[0], segments[1]
        return "UNKNOWN_ACTION", "MALFORMED_FRAME"


def child_node_runtime(pipe_endpoint) -> None:
    """Isolated compute loop processing system control codes over the active pipe context."""
    node = DuplexMessagingNode(pipe_endpoint)
    action, body = node.read_command()
    print(f"[CHILD] Intercepted incoming pipe execution directive: {action} with parameter [{body}]")
    
    if action == "COMPUTE_HASH":
        processed_response = f"HASH_METRIC_{os.getpid()}_SECURE"
        node.dispatch_command("COMPUTE_SUCCESS", processed_response)

if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe(duplex=True)
    
    worker_node = multiprocessing.Process(target=child_node_runtime, args=(child_conn,))
    worker_node.start()

    parent_node = DuplexMessagingNode(parent_conn)
    print("[PARENT] Dispatching structured framing directive across duplex channel...")
    parent_node.dispatch_command("COMPUTE_HASH", "PAYLOAD_BLOCK_991A")

    response_action, response_body = parent_node.read_command()
    print(f"[PARENT] Verified return confirmation sequence from worker: {response_action} -> {response_body}")
    
    worker_node.join()