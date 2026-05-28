"""
Core Topic: Application Layer Protocol Parsing
Description: Parses raw string payloads into valid, structured HTTP/1.1 objects.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Tuple

class CustomHTTPParser:
    @staticmethod
    def parse_request(raw_http_packet: str) -> Tuple[Dict[str, str], Dict[str, str], str]:
        """Deconstructs wire-level HTTP protocol blocks into explicit internal components."""
        lines = raw_http_packet.split("\r\n")
        metadata: Dict[str, str] = {}
        headers: Dict[str, str] = {}
        body = ""

        if not lines or lines[0] == "":
            return metadata, headers, body

        # 1. Isolate the initial Request Line protocol statement
        request_line = lines[0].split(" ")
        if len(request_line) >= 3:
            metadata["method"] = request_line[0]
            metadata["path"] = request_line[1]
            metadata["version"] = request_line[2]

        # 2. Iterate and parse out specific key-value header metadata
        idx = 1
        while idx < len(lines):
            line = lines[idx]
            if line == "":  # An empty line safely marks the start of the body segment
                idx += 1
                break
            if ":" in line:
                key, val = line.split(":", 1)
                headers[key.strip().lower()] = val.strip()
            idx += 1

        # 3. Consume any remaining string items as payload body data
        body = "\r\n".join(lines[idx:])
        return metadata, headers, body

if __name__ == "__main__":
    sample_packet = (
        "POST /api/v1/telemetry HTTP/1.1\r\n"
        "Host: localhost:8085\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 23\r\n"
        "\r\n"
        '{"node_status": "GREEN"}'
    )
    
    meta, head, payload = CustomHTTPParser.parse_request(sample_packet)
    print(f"Parsed Method: {meta.get('method')} | Target Route: {meta.get('path')}")
    print(f"Content-Type Header Value: {head.get('content-type')}")
    print(f"Payload Stream Content: {payload}")