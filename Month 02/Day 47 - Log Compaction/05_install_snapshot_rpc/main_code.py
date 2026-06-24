# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: InstallSnapshot RPC Frame Streaming
Description: Chunks large binary state snapshots into predictable network frames for slow follower nodes.
"""
from typing import Generator, Dict

class SnapshotFrameStreamer:
    @staticmethod
    def slice_snapshot_stream(raw_data: bytes, frame_size_bytes: int) -> Generator[Dict[str, any], None, None]:
        offset = 0
        total_length = len(raw_data)
        
        while offset < total_length:
            chunk = raw_data[offset:offset + frame_size_bytes]
            is_terminal = (offset + frame_size_bytes) >= total_length
            yield {
                "offset": offset,
                "payload": chunk,
                "done": is_terminal
            }
            offset += frame_size_bytes

if __name__ == "__main__":
    large_binary_payload = b"state_payload_stream_chunk_bytes_saad_irfan_engineering"
    stream_generator = SnapshotFrameStreamer.slice_snapshot_stream(large_binary_payload, frame_size_bytes=10)
    
    frames_list = list(stream_generator)
    assert len(frames_list) > 1
    assert frames_list[0]["offset"] == 0
    assert frames_list[-1]["done"] == True