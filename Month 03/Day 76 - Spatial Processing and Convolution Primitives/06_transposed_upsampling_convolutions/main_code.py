# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Transposed Convolution (Deconvolution / Upsampling)
Description: Increases spatial dimensionality using fractionally strided convolutions 
             by injecting zero-dilation boundaries between spatial pixels.
"""
import numpy as np  # type: ignore


class TransposedConvolutionEngine:
    @staticmethod
    def upsample_feature_map(feature_map: np.ndarray, filter_kernel: np.ndarray, stride: int = 2) -> np.ndarray:
        h, w = feature_map.shape
        f_h, f_w = filter_kernel.shape
        
        # 1. Inject zeros between elements (Fractional Striding / Dilation)
        out_h = (h - 1) * stride + f_h
        out_w = (w - 1) * stride + f_w
        upsampled_grid = np.zeros((out_h, out_w), dtype=np.float64)
        
        # 2. Scatter the input features across the expanded grid
        for i in range(h):
            for j in range(w):
                # Multiply scalar pixel against the entire kernel and project it
                # onto the output grid, accumulating overlapping regions
                target_y = i * stride
                target_x = j * stride
                
                upsampled_grid[target_y:target_y+f_h, target_x:target_x+f_w] += feature_map[i, j] * filter_kernel
                
        return upsampled_grid


if __name__ == "__main__":
    # Small 2x2 compressed feature map
    small_feature = np.array([
        [1.0, 2.0],
        [3.0, 4.0]
    ], dtype=np.float64)
    
    # 3x3 filter
    kernel = np.ones((3, 3), dtype=np.float64)
    
    upsampled_output = TransposedConvolutionEngine.upsample_feature_map(small_feature, kernel, stride=2)
    
    # Output should blow up to (2-1)*2 + 3 = 5x5 matrix
    assert upsampled_output.shape == (5, 5)
    # The absolute center pixel (2,2) receives overlapping sums from all 4 projected kernels
    assert upsampled_output[2, 2] == 10.0  # 1 + 2 + 3 + 4
    
    print(f"[TASK 06 PASSED] Transposed Convolution (Upsampling) successfully executed:\n{upsampled_output}")