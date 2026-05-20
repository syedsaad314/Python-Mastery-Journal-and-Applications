"""
Core Topic: Cryptographic Content-Based Data Deduplication
Description: Generating high-speed text hash fingerprints to purge redundant items from training sets.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import hashlib

class DatasetDeduplicator:
    def __init__(self):
        # Set containing uniquely identified asset finger-prints (O(1) lookups)
        self.seen_signatures = set()

    def _compute_sha256_hash(self, text_content: str) -> str:
        """Generates a secure, 64-character hexadecimal data fingerprint string."""
        normalized_string = text_content.strip().lower()
        return hashlib.sha256(normalized_string.encode('utf-8')).hexdigest()

    def process_document(self, content: str) -> tuple[bool, str]:
        """Checks if content signature exists, registering unique documents immediately."""
        signature = self._compute_sha256_hash(content)
        
        if signature in self.seen_signatures:
            return False, signature  # Flag document as a duplicate
            
        self.seen_signatures.add(signature)
        return True, signature  # Document is clean and original

if __name__ == "__main__":
    pipeline = DatasetDeduplicator()
    
    document_sample_a = "Clean unstructured data string targeted for model fine-tuning processes."
    document_sample_b = "Clean unstructured data string targeted for model fine-tuning processes."
    document_sample_c = "Alternative record entry destined for validation layers."
    
    print(f"Doc A Registration Status: {pipeline.process_document(document_sample_a)}")
    print(f"Doc B Registration Status (Duplicate Check): {pipeline.process_document(document_sample_b)}")
    print(f"Doc C Registration Status: {pipeline.process_document(document_sample_c)}")