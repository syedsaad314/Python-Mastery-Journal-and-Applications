"""
Core Topic: Message Delivery Guarantee Semantics
Description: Simulates processing paths for At-Least-Once vs Exactly-Once delivery guarantees.
Lead Engineer: Syed Saad Bin Irfan
"""

class DeliveryGuaranteeValidator:
    """Validates data state accuracy across different processing guarantee configurations."""
    
    @staticmethod
    def process_event_by_strategy(strategy: str, crash_midway: bool) -> str:
        """Simulates how different processing strategies handle mid-operation system crashes."""
        if strategy == "AT_LEAST_ONCE":
            # At-Least-Once: Process data first, then commit offset late
            # A crash midway means the offset is never committed, causing the message to be reprocessed later
            if crash_midway:
                return "PROCESSED_BUT_NOT_COMMITTED_WILL_DUPLICATE_ON_RETRY"
            return "SUCCESS_COMMITTED"
            
        elif strategy == "EXACTLY_ONCE":
            # Exactly-Once: Runs processing and offset commits atomically in a single transaction block
            if crash_midway:
                return "TRANSACTION_ABORTED_STATE_ROLLED_BACK_NO_DUPLICATES"
            return "SUCCESS_COMMITTED"
        return "UNKNOWN"


if __name__ == "__main__":
    validator = DeliveryGuaranteeValidator()
    # At-Least-Once can cause duplicate records if a crash occurs before the offset is committed
    res_1 = validator.process_event_by_strategy("AT_LEAST_ONCE", crash_midway=True)
    # Exactly-Once aborts cleanly and rolls back state safely if a failure happens midway
    res_2 = validator.process_event_by_strategy("EXACTLY_ONCE", crash_midway=True)
    
    print(f"[SEMANTICS] At-Least-Once Crash: {res_1}")
    print(f"[SEMANTICS] Exactly-Once Crash: {res_2}")