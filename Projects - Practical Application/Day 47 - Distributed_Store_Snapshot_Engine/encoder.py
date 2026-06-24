# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Binary Transformation Data Encoders
"""
import json
from typing import Dict, Any

class SnapshotEncoder:
    @staticmethod
    def export_to_binary_stream(structured_packet: Dict[str, Any]) -> bytes:
        # Generate clean compressed un-spaced layout format maps
        return json.dumps(structured_packet, separators=(',', ':')).encode('utf-8')

    @staticmethod
    def import_from_binary_stream(raw_bytes: bytes) -> Dict[str, Any]:
        return json.loads(raw_bytes.decode('utf-8'))