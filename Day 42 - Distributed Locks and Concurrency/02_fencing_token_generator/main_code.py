"""
Core Topic: Fencing Tokens Pattern
Description: Generates monotonically increasing tokens to prevent delayed out-of-order storage writes.
Lead Engineer: Syed Saad Bin Irfan
"""

class FencingTokenGenerator:
    """Generates sequential, unique tokens to protect data stores from out-of-order writes."""
    
    def __init__(self) -> None:
        self._current_token = 0

    def increment_and_get(self) -> int:
        self._current_token += 1
        return self._current_token

class MockSharedStorage:
    """Simulates a network storage layer that drops stale, out-of-order historical writes."""
    
    def __init__(self) -> None:
        self.last_accepted_token = 0
        self.stored_data = ""

    def commit_write(self, token: int, payload: str) -> bool:
        """Validates the incoming token, discarding it if a newer write has already been processed."""
        if token > self.last_accepted_token:
            self.last_accepted_token = token
            self.stored_data = payload
            return True
        print(f"[STORAGE-REJECT] Dropped write with stale token {token}. Last accepted was {self.last_accepted_token}.")
        return False


if __name__ == "__main__":
    generator = FencingTokenGenerator()
    storage = MockSharedStorage()

    token_a = generator.increment_and_get() # Token = 1
    token_b = generator.increment_and_get() # Token = 2

    # Simulate Node B executing its write instantly
    assert storage.commit_write(token_b, "Data from Node B") == True
    # Simulate Node A's delayed write arriving late due to a network hiccup
    assert storage.commit_write(token_a, "Data from Node A") == False