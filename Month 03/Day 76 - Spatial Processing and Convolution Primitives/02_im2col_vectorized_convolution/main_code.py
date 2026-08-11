# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Im2Col (Image to Column) Vectorized Convolution
Description: Converts the sliding window convolution operation into a highly 
             optimized single Dense Matrix Multiplication (GEMM) via memory reshaping.
"""
import numpy as np  # type: ignore


class Im2ColConvolutionEngine:
    @staticmethod
    def convolve_im2col(image: np.ndarray, filter_kernel: np.ndarray) -> np.ndarray:
        i_h, i_w = image.shape
        f_h, f_w = filter_kernel.shape
        
        out_h = i_h - f_h + 1
        out_w = i_w - f_w + 1
        
        # 1. Unroll the image into a matrix (Im2Col Operation)
        # Every receptive field window becomes a flat column
        col_matrix = np.zeros((f_h * f_w, out_h * out_w), dtype=np.float64)
        col_idx = 0
        for h in range(out_h):
            for w in range(out_w):
                # Flatten the window and store it as a column
                col_matrix[:, col_idx] = image[h:h+f_h, w:w+f_w].ravel()
                col_idx += 1
                
        # 2. Flatten the filter kernel into a single row vector
        kernel_row = filter_kernel.ravel().reshape(1, -1)
        
        # 3. Execute Vectorized Matrix Multiplication (BLAS GEMM)
        feature_vector = np.dot(kernel_row, col_matrix)
        
        # 4. Reshape the flat result back into the 2D spatial feature map
        return feature_vector.reshape(out_h, out_w)


if __name__ == "__main__":
    img = np.arange(1, 17, dtype=np.float64).reshape(4, 4)
    kernel = np.ones((2, 2), dtype=np.float64)
    
    convolved_feature = Im2ColConvolutionEngine.convolve_im2col(img, kernel)
    
    # 4x4 image with 2x2 kernel = 3x3 output
    assert convolved_feature.shape == (3, 3)
    # Top left = 1+2+5+6 = 14
    assert convolved_feature[0, 0] == 14.0
    
    print(f"[TASK 02 PASSED] Im2Col Matrix Unrolling resolved convolution flawlessly:\n{convolved_feature}")