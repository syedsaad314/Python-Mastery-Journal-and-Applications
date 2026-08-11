# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Max and Average Spatial Pooling
Description: Implements non-overlapping spatial reduction modules to downsample 
             feature maps, generating translation invariance and reducing compute overhead.
"""
import numpy as np  # type: ignore


class SpatialPoolingEngine:
    @staticmethod
    def max_pool_2d(feature_map: np.ndarray, pool_size: int = 2) -> np.ndarray:
        h, w = feature_map.shape
        out_h = h // pool_size
        out_w = w // pool_size
        
        # Reshape and take max across specific axes without explicit Python loops
        # Matrix is split into distinct pool_size blocks, then maxed out
        reshaped = feature_map[:out_h * pool_size, :out_w * pool_size].reshape(out_h, pool_size, out_w, pool_size)
        return reshaped.max(axis=(1, 3))

    @staticmethod
    def avg_pool_2d(feature_map: np.ndarray, pool_size: int = 2) -> np.ndarray:
        h, w = feature_map.shape
        out_h = h // pool_size
        out_w = w // pool_size
        
        reshaped = feature_map[:out_h * pool_size, :out_w * pool_size].reshape(out_h, pool_size, out_w, pool_size)
        return reshaped.mean(axis=(1, 3))


if __name__ == "__main__":
    f_map = np.array([
        [1, 3,  2, 4],
        [5, 6,  9, 1],
        [0, 2, -1, 3],
        [4, 8,  0, 2]
    ], dtype=np.float64)
    
    max_pooled = SpatialPoolingEngine.max_pool_2d(f_map, pool_size=2)
    avg_pooled = SpatialPoolingEngine.avg_pool_2d(f_map, pool_size=2)
    
    # 4x4 matrix pooled by 2x2 yields 2x2
    assert max_pooled.shape == (2, 2)
    
    # Max in top-left block: [1,3; 5,6] = 6
    assert max_pooled[0, 0] == 6.0
    # Avg in bottom-right block: [-1,3; 0,2] = (4/4) = 1.0
    assert avg_pooled[1, 1] == 1.0
    
    print(f"[TASK 03 PASSED] Vectorized Max and Average pooling matrices resolved down to dimension:\n{max_pooled}")