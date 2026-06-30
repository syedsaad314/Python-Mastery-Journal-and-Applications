# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Isolated Multi-Version Concurrency Replica Node
"""
from typing import Dict, List, Tuple
from models import VersionedPayload, NodeReconciliationResult
from vector_clock import VectorClockEngine

class MultiVersionReplicaNode:
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        # Multi-version map tracking active data records alongside causal lineages
        self.storage_vault: Dict[str, List[VersionedPayload]] = {}

    def local_write(self, key: str, value: str) -> VersionedPayload:
        """
        Handles local client mutations by advancing this node's causal clock.
        """
        current_versions = self.storage_vault.get(key, [])
        
        if not current_versions:
            base_clock = {self.node_id: 1}
        else:
            # Derive the baseline clock map by merging all active tracking maps
            merged_clock = {}
            for version in current_versions:
                merged_clock = VectorClockEngine.merge(merged_clock, version.vector_map)
            base_clock = VectorClockEngine.increment(merged_clock, self.node_id)

        new_payload = VersionedPayload(data_value=value, vector_map=base_clock)
        self.storage_vault[key] = [new_payload] # Clear old references on a clean local overwrite
        print(f"[REPLICA-{self.node_id}] Accepted local write -> Key: {key}, Value: {value}, Clock: {base_clock}")
        return new_payload

    def integrate_remote_payload(self, key: str, remote_payload: VersionedPayload) -> NodeReconciliationResult:
        """
        Integrates incoming peer payloads, performing causal ordering checks 
        to detect clean overwrites or multi-version concurrent conflicts.
        """
        if key not in self.storage_vault or not self.storage_vault[key]:
            self.storage_vault[key] = [remote_payload]
            return NodeReconciliationResult(remote_payload.data_value, remote_payload.vector_map, 1, "INITIAL_WRITE")

        local_versions = self.storage_vault[key]
        retained_versions: List[VersionedPayload] = []
        is_concurrent_with_all = True

        for local in local_versions:
            relation = VectorClockEngine.compare_ordering(remote_payload.vector_map, local.vector_map)
            
            if relation == "NEWER":
                # The incoming update replaces this obsolete local record
                pass 
            elif relation == "OLDER":
                # The incoming update is outdated; keep the current local record
                retained_versions.append(local)
                is_concurrent_with_all = False
            else:
                # The updates are concurrent or identical; both versions must be preserved
                retained_versions.append(local)

        if is_concurrent_with_all and remote_payload not in retained_versions:
            retained_versions.append(remote_payload)
            action = "CONCURRENT_CONFLICT_DETECTED"
        else:
            action = "CAUSAL_DOMINANCE_MUTATION"

        if not retained_versions:
            retained_versions.append(remote_payload)
            action = "CLEAN_OVERWRITE"

        self.storage_vault[key] = retained_versions
        
        # Calculate final state metrics for tracking purposes
        final_value = "/".join([v.data_value for v in retained_versions])
        final_clock = {}
        for v in retained_versions:
            final_clock = VectorClockEngine.merge(final_clock, v.vector_map)

        return NodeReconciliationResult(
            resolved_value=final_value,
            unified_clock=final_clock,
            siblings_count=len(retained_versions),
            action_taken=action
        )

    def execute_manual_merge(self, key: str, resolved_value: str) -> VersionedPayload:
        """
        Reconciles multi-version conflicts into a single unified record, 
        merging the vector clocks of all active branches.
        """
        current_versions = self.storage_vault.get(key, [])
        if len(current_versions) <= 1:
            return current_versions[0] if current_versions else None

        unified_clock = {}
        for version in current_versions:
            unified_clock = VectorClockEngine.merge(unified_clock, version.vector_map)

        # Advance the local clock to mark this reconciliation event
        final_clock = VectorClockEngine.increment(unified_clock, self.node_id)
        resolved_payload = VersionedPayload(data_value=resolved_value, vector_map=final_clock)
        
        self.storage_vault[key] = [resolved_payload]
        print(f"[REPLICA-{self.node_id}] Resolved conflict manually -> Key: {key}, Unified Value: {resolved_value}, Clock: {final_clock}")
        return resolved_payload