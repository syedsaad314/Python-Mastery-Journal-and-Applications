# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Histogram Binning (LightGBM Optimization)
Description: Discretizes massive continuous feature arrays into tight integer bins (uint8),
             dropping continuous sorting constraints from O(N log N) to O(N).
"""
import numpy as np  # type: ignore


class HistogramBinningEngine:
    @staticmethod
    def construct_bins(feature_data: np.ndarray, max_bins: int = 256) -> tuple[np.ndarray, np.ndarray]:
        # Drop NaNs and ensure 1D flat array for statistical binning
        valid_data = feature_data[~np.isnan(feature_data)]
        
        if len(valid_data) == 0:
            raise ValueError("Feature array contains no valid numerical data.")
            
        # 1. Create histogram bin boundaries based on percentile distributions
        # max_bins is typically 256 (fitting perfectly into 1-byte uint8 memory)
        percentiles = np.linspace(0, 100, max_bins)
        bin_edges = np.percentile(valid_data, percentiles)
        
        # Ensure bin edges are strictly unique
        bin_edges = np.unique(bin_edges)
        
        # 2. Map continuous values into discrete uint8 buckets using binary search (np.digitize)
        # Shift -1 so indices start at 0
        binned_indices = np.digitize(feature_data, bin_edges) - 1
        
        # Force type downcasting to 8-bit integers to minimize RAM footprint
        binned_data_uint8 = binned_indices.astype(np.uint8)
        
        return binned_data_uint8, bin_edges


if __name__ == "__main__":
    np.random.seed(42)
    # Generate 1 Million continuous floating-point values
    massive_continuous_array = np.random.randn(1_000_000) * 100.0
    
    binned_array, edges = HistogramBinningEngine.construct_bins(massive_continuous_array, max_bins=255)
    
    # Assert data downcasted to unsigned 8-bit integers
    assert binned_array.dtype == np.uint8
    assert binned_array.shape == (1_000_000,)
    assert len(edges) <= 255
    
    # Maximum value in uint8 is 255
    assert np.max(binned_array) <= 255
    
    print(f"[TASK 05 PASSED] Continuous float array of size {len(massive_continuous_array)} discretized into uint8 bins successfully.")