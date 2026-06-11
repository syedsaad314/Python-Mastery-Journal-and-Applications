"""
Core Topic: Causal Delivery Network Middleware Simulation
Description: Buffers incoming messages and delays delivery until all causal prerequisites are satisfied.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, List, Tuple

class CausalDeliveryMiddleware:
    """Intercepts and holds network traffic, delivering messages only when their causal history matches."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.local_vector: Dict[str, int] = {}
        self.holdback_buffer: List[Tuple[str, Dict[str, int], str]] = []

    def process_incoming_packet(self, sender_id: str, sender_vector: Dict[str, int], payload: str) -> List[str]:
        """Buffers an incoming message and releases any queued messages whose causal conditions are met."""
        self.holdback_buffer.append((sender_id, sender_vector, payload))
        delivered_messages: List[str] = []
        progress_made = True
        
        while progress_made:
            progress_made = False
            for packet in list(self.holdback_buffer):
                s_id, s_vec, msg = packet
                
                # Check if the message's causal prerequisites are met
                prereqs_satisfied = True
                for k, required_tick in s_vec.items():
                    if k == s_id:
                        # The sender's counter must be exactly 1 step ahead of our last delivered message from them
                        if required_tick != self.local_vector.get(s_id, 0) + 1:
                            prereqs_satisfied = False
                            break
                    else:
                        # For all other nodes, the message shouldn't require a state newer than what we've already processed
                        if required_tick > self.local_vector.get(k, 0):
                            prereqs_satisfied = False
                            break
                            
                if prereqs_satisfied:
                    self.local_vector[s_id] = s_vec[s_id]
                    delivered_messages.append(msg)
                    self.holdback_buffer.remove(packet)
                    progress_made = True
                    
        return delivered_messages


if __name__ == "__main__":
    middleware = CausalDeliveryMiddleware("receiver_node")
    
    # Simulate network jitter where an out-of-order message arrives early
    # Msg 2 depends on Msg 1, but arrives first
    msg_2_vector = {"sender_a": 2} 
    msg_1_vector = {"sender_a": 1}
    
    print("[MIDDLEWARE] Processing out-of-order message 2 (Prerequisite count: 2)...")
    out1 = middleware.process_incoming_packet("sender_a", msg_2_vector, "Payload-Data-Step-Two")
    print(f" -> Delivered messages: {out1} (Buffered due to missing causal link)")
    
    print("[MIDDLEWARE] Processing missing message 1...")
    out2 = middleware.process_incoming_packet("sender_a", msg_1_vector, "Payload-Data-Step-One")
    print(f" -> Delivered messages: {out2} (Causal link satisfied, releasing buffered frames)")