"""
CORE CONCEPT: Structured K-Way List Merge Sort Engine
Combining multiple pre-sorted arrays into a single unified output stream.
Tracks stream state across active arrays to manage data consolidation efficiently.
"""

class KWayMergeEngine:
    @staticmethod
    def merge_sorted_streams(streams: list[list[float]]) -> list[float]:
        """Merges multiple sorted arrays into a unified list using an active index matrix."""
        result = []
        # Track our current reading index pointer for each individual stream
        pointers = [0] * len(streams)
        
        while True:
            smallest_value = float('inf')
            target_stream_idx = -1
            
            # Identify the smallest available element across all active pointers
            for i, stream in enumerate(streams):
                if pointers[i] < len(stream):
                    if stream[pointers[i]] < smallest_value:
                        smallest_value = stream[pointers[i]]
                        target_stream_idx = i
                        
            # If no elements remain across any streams, sorting is complete
            if target_stream_idx == -1:
                break
                
            result.append(smallest_value)
            pointers[target_stream_idx] += 1
            
        return result


if __name__ == "__main__":
    s1 = [10.2, 40.5, 70.8]
    s2 = [20.1, 50.4, 80.9]
    s3 = [5.2, 30.7, 99.1]
    
    combined = KWayMergeEngine.merge_sorted_streams([s1, s2, s3])
    print(f"Unified Sorted Output Array: {combined}")