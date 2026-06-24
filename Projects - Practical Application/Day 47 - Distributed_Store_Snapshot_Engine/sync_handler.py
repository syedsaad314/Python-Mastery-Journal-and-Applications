# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Network RPC Transmission Chunkers
"""
from typing import Generator, Dict, Any

class SnapshotTransmissionHandler:
    @staticmethod
    def package_network_chunks(raw_image: bytes, maximum_transmission_unit: int) -> Generator[Dict[str, Any], None, None]:
        current_offset = 0
        total_data_size = len(raw_image)
        
        while current_offset < total_data_size:
            chunk_slice = raw_image[current_offset:current_offset + maximum_transmission_unit]
            current_offset += maximum_transmission_unit
            yield {
                "offset": current_offset - maximum_transmission_unit,
                "data_chunk": chunk_slice,
                "transmission_complete": current_offset >= total_data_size
            }