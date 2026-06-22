"""
Core Topic: Low-Level Async Raw HTTP Transport Engine
Description: Connects directly via TCP streams to parse raw HTTP header lines manually.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio

async def fetch_raw_http_headers(target_host: str) -> str:
    """Dispatches a raw HTTP GET instruction stream over a plain TCP connection."""
    print(f"[RAW-HTTP] Constructing underlying socket wire mapping to {target_host}...")
    
    # Establish direct TCP stream connections over port 80
    reader, writer = await asyncio.open_connection(target_host, 80)
    
    # Structure valid plain-text raw HTTP payload commands
    raw_http_request = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    
    writer.write(raw_http_request.encode('utf-8'))
    await writer.drain() # Flush packet wire arrays completely

    print("[RAW-HTTP] Stream dispatched. Intercepting response lines...")
    first_response_line = await reader.readline()
    sanitized_output = first_response_line.decode('utf-8').strip()
    
    writer.close()
    await writer.wait_closed()
    return sanitized_output

async def main() -> None:
    # Use a highly stable target domain for clean resolution tests
    domain_target = "example.com"
    http_status_line = await fetch_raw_http_headers(domain_target)
    print(f"[RAW-HTTP] Received status resolution signature: {http_status_line}")

if __name__ == "__main__":
    asyncio.run(main())