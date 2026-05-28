"""
Core Topic: Remote Procedure Call (RPC) Internals
Description: Executes structured function mappings across networked microservice nodes using serialization.
Lead Engineer: Syed Saad Bin Irfan
"""

import json
from typing import Callable, Dict, Any

class RPCFramework:
    def __init__(self) -> None:
        self.procedure_registry: Dict[str, Callable[..., Any]] = {}

    def register_procedure(self, name: str, procedure_callable: Callable[..., Any]) -> None:
        """Binds a standard function component directly to the RPC runtime router mechanism."""
        self.procedure_registry[name] = procedure_callable

    def dispatch_wire_payload(self, raw_json_request: str) -> str:
        """Processes an incoming RPC wire packet, fires the targeted method, and returns a serialized result."""
        try:
            payload = json.loads(raw_json_request)
            method_name = payload.get("method")
            arguments = payload.get("args", [])
            kwargs = payload.get("kwargs", {})

            if method_name not in self.procedure_registry:
                return json.dumps({"jsonrpc": "2.0", "error": "METHOD_NOT_FOUND", "id": payload.get("id")})

            # Execute the matching method using parameter unpacking unpacking
            execution_result = self.procedure_registry[method_name](*arguments, **kwargs)
            return json.dumps({"jsonrpc": "2.0", "result": execution_result, "id": payload.get("id")})

        except Exception as err:
            return json.dumps({"jsonrpc": "2.0", "error": f"INTERNAL_EXCEPTION::{str(err)}", "id": None})

# Sample function for network verification
def compute_server_load(core_count: int, utilization_rate: float) -> float:
    return core_count * utilization_rate

if __name__ == "__main__":
    rpc_node = RPCFramework()
    rpc_node.register_procedure("metrics.get_load", compute_server_load)
    
    # Mocking a wire-level network packet call
    mock_packet = '{"jsonrpc": "2.0", "method": "metrics.get_load", "args": [8, 0.65], "id": 101}'
    response_packet = rpc_node.dispatch_wire_payload(mock_packet)
    print(f"RPC Node Wire Response: {response_packet}")