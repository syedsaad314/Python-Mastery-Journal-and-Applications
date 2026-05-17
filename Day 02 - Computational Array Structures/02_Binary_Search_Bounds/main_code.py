"""
CORE CONCEPT: Binary Search Upper and Lower Bound Boundary Engines
Building structural logarithmic search algorithms from scratch that locate exact matching
indices and calculate data split thresholds within sorted lists.
"""

class BoundarySearchEngine:
    @staticmethod
    def lower_bound(array: list[float], target: float) -> int:
        """Finds the lowest index where target can be inserted while keeping the array sorted."""
        low, high = 0, len(array)
        
        while low < high:
            mid = (low + high) // 2
            if array[mid] < target:
                low = mid + 1
            else:
                high = mid
                
        return low

    @staticmethod
    def upper_bound(array: list[float], target: float) -> int:
        """Finds the highest index where target can be inserted while keeping the array sorted."""
        low, high = 0, len(array)
        
        while low < high:
            mid = (low + high) // 2
            if array[mid] <= target:
                low = mid + 1
            else:
                high = mid
                
        return low


if __name__ == "__main__":
    sorted_features = [1.2, 2.4, 4.5, 4.5, 4.5, 5.8, 7.1]
    
    lbl = BoundarySearchEngine.lower_bound(sorted_features, 4.5)
    ubl = BoundarySearchEngine.upper_bound(sorted_features, 4.5)
    
    print(f"Lower Bound Index (First Occurrence): {lbl}")
    print(f"Upper Bound Index (Boundary Limit): {ubl}")