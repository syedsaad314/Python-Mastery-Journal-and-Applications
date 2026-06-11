"""
System: Distributed Causal Chat Messaging Engine
Description: End-to-end multi-client chat simulation tracking conversation causality 
             vectors to prevent out-of-order race conditions over unstable channels.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import List, Dict, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (CausalChat-Mesh) %(message)s')

class ChatMessagePacket:
    """Encapsulates a message payload along with its causal dependencies."""
    
    def __init__(self, sender: str, text: str, dependencies_vector: Dict[str, int]) -> None:
        self.sender: str = sender
        self.text: str = text
        self.dependencies_vector: Dict[str, int] = dependencies_vector


class ChatClientNode:
    """Represents a decentralized chat user who sends and causally orders text messages."""
    
    def __init__(self, username: str) -> None:
        self.username: str = username
        self.vector_clock: Dict[str, int] = {username: 0}
        self.visible_chat_history: List[str] = []
        self.incoming_holdback_buffer: List[ChatMessagePacket] = []

    def dispatch_chat_message(self, text: str) -> ChatMessagePacket:
        """Sends a new chat message and updates the client's local vector clock."""
        self.vector_clock[self.username] = self.vector_clock.get(self.username, 0) + 1
        logging.info(f"[{self.username}] Dispatching message: '{text}' | Clock: {self.vector_clock}")
        return ChatMessagePacket(self.username, text, dict(self.vector_clock))

    def ingest_network_packet(self, packet: ChatMessagePacket) -> None:
        """Buffers incoming messages and releases them into the history once causal constraints are met."""
        self.incoming_holdback_buffer.append(packet)
        self.flush_runnable_buffer_entries()

    def flush_runnable_buffer_entries(self) -> None:
        """Iterates over buffered messages and updates the chat history as dependencies are resolved."""
        progress_made = True
        while progress_made:
            progress_made = False
            for packet in list(self.incoming_holdback_buffer):
                sender = packet.sender
                vec = packet.dependencies_vector
                
                # Verify that all causal prerequisites are satisfied
                is_runnable = True
                for node, count in vec.items():
                    if node == sender:
                        if count != self.vector_clock.get(sender, 0) + 1:
                            is_runnable = False
                            break
                    else:
                        if count > self.vector_clock.get(node, 0):
                            is_runnable = False
                            break
                            
                if is_runnable:
                    # Append to visible history and update local clock trackers
                    self.vector_clock[sender] = vec[sender]
                    self.visible_chat_history.append(f"<{sender}> {packet.text}")
                    self.incoming_holdback_buffer.remove(packet)
                    progress_made = True


if __name__ == "__main__":
    print("\n=== STARTING CAUSAL CHAT CORE REPLICATED TOPOLOGY ===\n")
    
    # Instantiate chat participants
    client_saad  = ChatClientNode("Saad")
    client_fabha = ChatClientNode("Fabha")
    
    # Saad sends an initial message
    pkt_1 = client_saad.dispatch_chat_message("Are we deploying the cluster update today?")
    
    # Fabha reads Saad's message and responds
    client_fabha.ingest_network_packet(pkt_1)
    pkt_2 = client_fabha.dispatch_chat_message("Yes, as soon as the test logs pass cleanly.")
    
    # Simulate network jitter where Fabha's response arrives at a node before Saad's initial question
    print("\n[NETWORK-ANOMALY] Simulating out-of-order message arrival at a third node...")
    observer_node = ChatClientNode("AuditorNode")
    
    logging.info("AuditorNode receives Fabha's reply first...")
    observer_node.ingest_network_packet(pkt_2)
    print(f" -> Auditor visible feed: {observer_node.visible_chat_history} (Held back to maintain conversational flow)")
    
    logging.info("AuditorNode receives Saad's initial question...")
    observer_node.ingest_network_packet(pkt_1)
    print(f" -> Auditor visible feed: {observer_node.visible_chat_history} (Causality satisfied, full feed released)")
    
    print("\n=== SYSTEM SHUTDOWN: CHAT CORE ENGINE TERMINATED ===")