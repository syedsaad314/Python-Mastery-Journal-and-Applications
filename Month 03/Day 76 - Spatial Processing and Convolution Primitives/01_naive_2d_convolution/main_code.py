# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Naive 2D Convolution Primitive
Description: Computes spatial feature extraction using raw sliding-window mathematical 
             loops to demonstrate the foundational cross-correlation algorithm.
"""
import numpy as np  # type: ignore


class NaiveConvolutionEngine:
    @staticmethod
    def convolve_2d(image: np.ndarray, filter_kernel: np.ndarray) -> np.ndarray:
        # Validate 2D dimensions
        if image.ndim != 2 or filter_kernel.ndim != 2:
            raise ValueError("Naive convolution strictly accepts 2D matrices.")
            
        i_h, i_w = image.shape
        f_h, f_w = filter_kernel.shape
        
        # Calculate output dimensions (Stride=1, Padding=0)
        out_h = i_h - f_h + 1
        out_w = i_w - f_w + 1
        output = np.zeros((out_h, out_w), dtype=np.float64)
        
        # O(N*M*K*L) Nested Loop Cross-Correlation
        for h in range(out_h):
            for w in range(out_w):
                # Extract the spatial receptive field window
                receptive_field = image[h:h+f_h, w:w+f_w]
                # Element-wise multiplication and summation
                output[h, w] = np.sum(receptive_field * filter_kernel)
                
        return output


if __name__ == "__main__":
    # 4x4 Input Image
    img = np.array([
        [1, 2, 3, 0],
        [0, 1, 2, 3],
        [3, 0, 1, 2],
        [2, 3, 0, 1]
    ], dtype=np.float64)
    
    # 3x3 Edge Detection Filter
    kernel = np.array([
        [ 1,  0, -1],
        [ 1,  0, -1],
        [ 1,  0, -1]
    ], dtype=np.float64)
    
    convolved_feature = NaiveConvolutionEngine.convolve_2d(img, kernel)
    
    # Output shape should be (4-3+1, 4-3+1) = (2, 2)
    assert convolved_feature.shape == (2, 2)
    
    # Verify top-left pixel evaluation
    assert convolved_feature[0, 0] == ((1*1 + 2*0 + 3*-1) + (0*1 + 1*0 + 2*-1) + (3*1 + 0*0 + 1*-1))
    
    print(f"[TASK 01 PASSED] Naive 2D Convolution mapped spatial features successfully:\n{convolved_feature}")