# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Unified Engine Read-Path System Orchestrator
"""
import time
from models import ClientRequest, ReadQuery
from lease_manager import SystemLeaseManager
from read_index_engine import ReadIndexEngine
from session_store import IdempotentSessionStore
from kv_replica import KVReplicaStore

class LinearizableEngineOrchestrator:
    def __init__(self, cluster_nodes: list) -> None:
        self.lease_mgr = SystemLeaseManager(baseline_duration=1.5, max_drift_factor=5.0)
        self.read_idx_engine = ReadIndexEngine(cluster_nodes)
        self.sessions = IdempotentSessionStore()
        self.storage = KVReplicaStore()

    def process_mutation_transaction(self, request: ClientRequest) -> dict:
        # Check for cached duplicate requests to ensure idempotency
        cached_res = self.sessions.fetch_cached_response(request.client_id, request.sequence_id)
        if cached_res is not  None:
            return {"execution_status": "IDEMPOTENT_CACHE_HIT", "result": cached_res, "retried": True}

        # Execute the write mutation against the local state machine
        execution_output = self.storage.execute_local_mutation(request.payload)
        
        # Cache the result before returning it to the client
        self.sessions.cache_session_transaction(request.client_id, request.sequence_id, execution_output)
        return {"execution_status": "FRESH_MUTATION_COMMITTED", "result": execution_output, "retried": False}

    def process_linearizable_read(self, key: str, mock_active_network_acks: list) -> dict:
        start_time = time.time()
        
        # Strategy 1: Check if the leader lease is still active and valid
        if self.lease_mgr.confirm_safe_read_authority():
            read_data = self.storage.execute_local_read(key)
            return {
                "read_strategy": "LOCAL_LEASE_READ",
                "resolved_index": self.read_idx_engine.current_leader_commit_index,
                "data": read_data,
                "latency_profile": "optimized_low_latency"
            }
            
        # Strategy 2: Lease expired fallback. Run a full ReadIndex quorum verification pass.
        print("\n[ORCHESTRATOR-FALLBACK] Lease validation window closed. Initializing network quorum route...")
        target_read_index = self.read_idx_engine.establish_read_index_checkpoint()
        
        if self.read_idx_engine.validate_quorum_acknowledgments(mock_active_network_acks):
            read_data = self.storage.execute_local_read(key)
            return {
                "read_strategy": "QUORUM_READ_INDEX_FALLBACK",
                "resolved_index": target_read_index,
                "data": read_data,
                "latency_profile": "network_consensus_roundtrip"
            }
            
        return {
            "read_strategy": "READ_REJECTED_CONSISTENCY_FAILURE",
            "resolved_index": -1,
            "data": "SPLIT_BRAIN_WARNING_STALE_PREVENTION",
            "latency_profile": "failed_verification"
        }