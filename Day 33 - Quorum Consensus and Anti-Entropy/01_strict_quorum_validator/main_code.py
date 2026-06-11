"""
Core Topic: Strict Quorum Consensus Validator
Description: Models node cluster availability and validates strict quorum requirements.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Tuple

class QuorumValidator:
    """Evaluates cluster read/write configuration parameters to guarantee data overlap."""
    
    def __init__(self, total_replicas: int, write_quorum: int, read_quorum: int) -> None:
        self.n = total_replicas  # N: Replication Factor
        self.w = write_quorum     # W: Write Quorum Count
        self.r = read_quorum      # R: Read Quorum Count

    def is_quorum_strict(self) -> bool:
        """Verifies if the quorum configuration guarantees that at least one node overlaps."""
        return (self.w + self.r) > self.n

    def evaluate_operation_survives(self, healthy_nodes_count: int) -> Dict[str, bool]:
        """Determines if the cluster can successfully process reads and writes with current healthy nodes."""
        return {
            "write_executable": healthy_nodes_count >= self.w,
            "read_executable": healthy_nodes_count >= self.r
        }


if __name__ == "__main__":
    # Standard Dynamo-style deployment setup: N=3, W=2, R=2
    validator = QuorumValidator(total_replicas=3, write_quorum=2, read_quorum=2)
    
    print(f"[QUORUM-VALIDATOR] Configuration Strictness Profile: {validator.is_quorum_strict()}")
    
    # Simulate a network partition where only 1 replica out of 3 is reachable
    cluster_health_metrics = validator.evaluate_operation_survives(healthy_nodes_count=1)
    print(f" -> Cluster availability status with 1 healthy node: {cluster_health_metrics}")