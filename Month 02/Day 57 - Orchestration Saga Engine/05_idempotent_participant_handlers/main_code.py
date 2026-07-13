# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Idempotent Participant Message Handlers
Description: Protects participant endpoints against network retries by tracking 
             and deduplicating requests using incoming correlation IDs.
"""
from typing import Dict, Any

class IdempotentParticipantHandler:
    def __init__(self) -> None:
        self.deduplication_ledger: Dict[str, Dict[str, Any]] = {}

    def process_transactional_request(self, correlation_id: str, action_payload: Dict[str, Any]) -> Dict[str, Any]:
        # If the token exists, return the cached result immediately instead of re-running
        if correlation_id in self.deduplication_ledger:
            return {**self.deduplication_ledger[correlation_id], "deduplicated": True}

        # Simulate executing the unique write operation
        execution_result = {"status": "PROCESSED", "resource_id": action_payload.get("id")}
        self.deduplication_ledger[correlation_id] = execution_result
        return {**execution_result, "deduplicated": False}

if __name__ == "__main__":
    handler = IdempotentParticipantHandler()
    req_payload = {"id": "item_90"}
    
    res_1 = handler.process_transactional_request("msg_token_1", req_payload)
    res_2 = handler.process_transactional_request("msg_token_1", req_payload)
    
    assert res_1["deduplicated"] is False
    assert res_2["deduplicated"] is True
    assert res_2["status"] == "PROCESSED"