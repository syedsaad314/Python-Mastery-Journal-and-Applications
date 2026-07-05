# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Event-Driven Raft Consensus Node State Machine
"""
import random
from models import VoteRequest, VoteResponse, AppendEntriesHeartbeat
from network_stub import MockNetworkBackplane

class RaftConsensusNode:
    def __init__(self, node_id: str, network_ref: MockNetworkBackplane) -> None:
        self.node_id = node_id
        self.network = network_ref
        
        # Core Raft State Variables
        self.current_term: int = 0
        self.voted_for: Optional[str] = None # type: ignore
        self.state: str = "FOLLOWER" # "FOLLOWER", "CANDIDATE", "LEADER"
        
        # Simulated Tracking Parameters
        self.heartbeats_received: int = 0

    def trigger_election_timeout(self, total_nodes: int) -> bool:
        """
        Simulates an election timeout. The node transitions to Candidate status 
        and solicits votes from across the cluster network.
        """
        if self.state == "LEADER":
            return False

        print(f"\n[RAFT-NODE-{self.node_id}] ! Election timeout triggered. Starting election campaign.")
        self.state = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id
        
        # Self vote counts toward securing a majority
        votes_secured = 1 
        req = VoteRequest(term=self.current_term, candidate_id=self.node_id)
        
        # Broadcast vote request requests to all network peers
        responses = self.network.broadcast_vote_request(self.node_id, req)
        
        for resp in responses:
            if resp.term > self.current_term:
                # Step down if we encounter a higher logical term counter
                self.current_term = resp.term
                self.state = "FOLLOWER"
                self.voted_for = None
                return False
            if resp.vote_granted:
                votes_secured += 1

        majority_limit = (total_nodes // 2) + 1
        print(f"[RAFT-NODE-{self.node_id}] Ballot Box Result: Secured {votes_secured}/{total_nodes} votes.")
        
        if votes_secured >= majority_limit and self.state == "CANDIDATE":
            self.state = "LEADER"
            print(f"[RAFT-NODE-{self.node_id}] ★ Success! Elected Cluster Leader for term {self.current_term}.")
            return True
            
        self.state = "FOLLOWER"
        return False

    def receive_vote_rpc(self, request: VoteRequest) -> VoteResponse:
        """
        Processes vote requests from candidate peers. Enforces term limits 
        and ensures only one vote is cast per term.
        """
        if request.term > self.current_term:
            self.current_term = request.term
            self.state = "FOLLOWER"
            self.voted_for = None

        if request.term == self.current_term and (self.voted_for is None or self.voted_for == request.candidate_id):
            self.voted_for = request.candidate_id
            print(f"[RAFT-NODE-{self.node_id}] Vote GRANTED to candidate: {request.candidate_id} for term {self.current_term}")
            return VoteResponse(term=self.current_term, vote_granted=True, responder_id=self.node_id)
            
        print(f"[RAFT-NODE-{self.node_id}] Vote DENIED to candidate: {request.candidate_id} for term {request.term}")
        return VoteResponse(term=self.current_term, vote_granted=False, responder_id=self.node_id)

    def receive_heartbeat_rpc(self, heartbeat: AppendEntriesHeartbeat) -> None:
        """
        Processes leader heartbeats to suppress local elections.
        """
        if heartbeat.term >= self.current_term:
            self.current_term = heartbeat.term
            self.state = "FOLLOWER"
            self.voted_for = None
            self.heartbeats_received += 1
            print(f"[RAFT-NODE-{self.node_id}] Heartbeat received from leader '{heartbeat.leader_id}'. Resetting election timer.")