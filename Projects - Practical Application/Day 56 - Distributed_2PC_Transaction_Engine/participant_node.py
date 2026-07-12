# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Transaction Participant Node with Write-Ahead State Mechanics
"""
from typing import Dict, Any, Optional
from models import TransactionPayload, TransactionCommand, ParticipantVote

class TransactionParticipantNode:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        
        # Internal Storage Layouts
        self.durable_wal_log: list[str] = []
        self.active_data_store: Dict[str, Any] = {}
        self.isolated_workspaces: Dict[str, Any] = {}

    def receive_transaction_rpc(self, msg: TransactionPayload) -> ParticipantVote:
        tx_id = msg.tx_id
        
        # Phase 1: Prepare Command Handling
        if msg.command == TransactionCommand.PREPARE:
            # Check for data conflicts or explicit error triggers
            if msg.payload_data.get("value") == "TRIGGER_REJECTION_FAULT":
                self.durable_wal_log.append(f"WAL_ABORT_RECORD:{tx_id}")
                return ParticipantVote.VOTE_ABORT
                
            # Isolate the data write inside a temporary workspace and write to the WAL
            self.isolated_workspaces[tx_id] = msg.payload_data
            self.durable_wal_log.append(f"WAL_PREPARE_RECORD:{tx_id}")
            return ParticipantVote.VOTE_COMMIT

        # Phase 2: Finalization Commands
        elif msg.command == TransactionCommand.COMMIT:
            if tx_id in self.isolated_workspaces:
                # Move data from the isolated workspace into production storage
                data = self.isolated_workspaces.pop(tx_id)
                self.active_data_store[data["key"]] = data["value"]
                self.durable_wal_log.append(f"WAL_COMMIT_RECORD:{tx_id}")
            return ParticipantVote.VOTE_COMMIT

        elif msg.command == TransactionCommand.ABORT:
            # Drop the isolated workspace and clear pending locks
            self.isolated_workspaces.pop(tx_id, None)
            self.durable_wal_log.append(f"WAL_ABORT_RECORD:{tx_id}")
            return ParticipantVote.VOTE_ABORT

        return ParticipantVote.VOTE_ABORT