"""
Core Topic: Sliding Window Log Rate Limiter
Description: Tracking granular API timestamps inside dictionary vectors to enforce ingestion boundaries.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import time

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_duration_seconds: float):
        self.max_requests = max_requests
        self.window_duration = window_duration_seconds
        # User ID mapped to a list of micro-second timestamps
        self.user_logs = {}

    def request_allowed(self, user_id: str) -> bool:
        """Determines if an incoming request falls within acceptable window velocity limits."""
        current_timestamp = time.time()
        
        if user_id not in self.user_logs:
            self.user_logs[user_id] = []
            
        request_history = self.user_logs[user_id]
        
        # Prune outdated timestamps that fall outside the active window boundary
        cutoff_time = current_timestamp - self.window_duration
        while request_history and request_history[0] < cutoff_time:
            request_history.pop(0)
            
        # Evaluate current capacity
        if len(request_history) < self.max_requests:
            request_history.append(current_timestamp)
            return True
            
        return False

if __name__ == "__main__":
    limiter = SlidingWindowRateLimiter(max_requests=2, window_duration_seconds=1.0)
    client_identity = "gateway_ip_192_168_1_5"
    
    print(f"Request 01 Status: {limiter.request_allowed(client_identity)}")
    print(f"Request 02 Status: {limiter.request_allowed(client_identity)}")
    print(f"Request 03 Status (Expected Block): {limiter.request_allowed(client_identity)}")
    
    print("Simulating network propagation delay...")
    time.sleep(1.1)
    
    print(f"Request 04 Status (Post Window Reset): {limiter.request_allowed(client_identity)}")