"""
Mini-Project: In-Memory Secured Vault Utility
Description: Secures sensitive credentials in local memory by running immediate byte obfuscation transformations.
Lead Engineer: Syed Saad Bin Irfan
"""

import base64
import json
import time
from typing import Dict, List, Optional

class SecuredMemoryVault:
    def __init__(self, key_signature: str) -> None:
        self._storage: Dict[str, bytes] = {}
        self._logs: List[Dict[str, str]] = []
        self._mask = key_signature.encode('utf-8')

    def _xor_cipher(self, input_text: str) -> bytes:
        """Applies a reversible XOR transformation to prevent plaintext values from exposure in memory dumps."""
        encoded_bytes = input_text.encode('utf-8')
        scrambled = bytearray()
        for idx, byte in enumerate(encoded_bytes):
            scrambled.append(byte ^ self._mask[idx % len(self._mask)])
        return base64.b64encode(scrambled)

    def _xor_decipher(self, cipher_bytes: bytes) -> str:
        raw_binary = base64.b64decode(cipher_bytes)
        unscrambled = bytearray()
        for idx, byte in enumerate(raw_binary):
            unscrambled.append(byte ^ self._mask[idx % len(self._mask)])
        return unscrambled.decode('utf-8')

    def write_secret(self, key: str, value: str) -> None:
        self._storage[key] = self._xor_cipher(value)
        self._logs.append({"op": "WRITE", "key": key, "time": time.strftime("%H:%M:%S")})

    def read_secret(self, key: str) -> Optional[str]:
        if key not in self._storage:
            self._logs.append({"op": "REJECTED", "key": key, "time": time.strftime("%H:%M:%S")})
            return None
        self._logs.append({"op": "READ", "key": key, "time": time.strftime("%H:%M:%S")})
        return self._xor_decipher(self._storage[key])

if __name__ == "__main__":
    vault = SecuredMemoryVault("UBIT_SYS_ARCH_2026")
    vault.write_secret("DATABASE_PASSWORD", "SaadAdmin@2026")
    
    print("[PORTFOLIO SHOWCASE] In-Memory Obfuscated Representation:")
    print(f"Stored Byte Value: {vault._storage['DATABASE_PASSWORD'].decode('utf-8')}")
    
    decrypted = vault.read_secret("DATABASE_PASSWORD")
    print(f"Decrypted Runtime Value: {decrypted}")