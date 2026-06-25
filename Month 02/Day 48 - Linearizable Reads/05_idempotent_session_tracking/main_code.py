# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Client Session Idempotency Tracking
Description: Stores transaction sequence numbers to prevent duplicate command 
             execution when clients retry network requests.
"""
from typing import Dict, Any

class IdempotentSessionTracker:
    def __init__(self) -> None:
        self.session_history: Dict[str, Dict[int, Any]] = {}

    def register_and_evaluate_request(self, client_id: str, seq_id: int, command: str) -> Dict[str, Any]:
        if client_id not in self.session_history:
            self.session_history[client_id] = {}
            
        # If the sequence ID already exists, return the cached response immediately
        if seq_id in self.session_history[client_id]:
            print(f"[IDEMPOTENCY] Duplicate hit detected for Client '{client_id}' (Seq: {seq_id}). Serving cache.")
            return self.session_history[client_id][seq_id]

        # Execute the new mutation and cache the result
        execution_result = {"status": "SUCCESS", "mutated_cmd": command, "cached": False}
        self.session_history[client_id][seq_id] = {**execution_result, "cached": True}
        return execution_result

if __name__ == "__main__":
    tracker = IdempotentSessionTracker()
    
    res_1 = tracker.register_and_evaluate_request("client_saad", 4801, "APPEND item_list")
    res_2 = tracker.register_and_evaluate_request("client_saad", 4801, "APPEND item_list")
    
    assert res_1["cached"] == False
    assert res_2["cached"] == True
    assert res_1["mutated_cmd"] == res_2["mutated_cmd"]