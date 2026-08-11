# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Strided Mathematics and Zero-Padding
Description: Computes accurate bounding boxes for spatial features, ensuring 
             edge-pixel information is preserved using border padding calculations.
"""
import numpy as np  # type: ignore


class ConvolutionPaddingEngine:
    @staticmethod
    def calculate_output_shape(i_size: int, f_size: int, stride: int, padding: int) -> int:
        # Output spatial formula: O = floor((W - K + 2P) / S) + 1
        output_dim = ((i_size - f_size + (2 * padding)) // stride) + 1
        return output_dim

    @staticmethod
    def pad_image(image: np.ndarray, pad_size: int) -> np.ndarray:
        if pad_size < 0:
            raise ValueError("Padding size cannot be negative.")
        
        # Apply constant zero-padding to both Height and Width axes
        return np.pad(image, pad_width=pad_size, mode='constant', constant_values=0)


if __name__ == "__main__":
    raw_image = np.ones((5, 5), dtype=np.float64)
    
    # Goal: Preserve 5x5 spatial volume using a 3x3 filter (Stride=1)
    # P = (K - 1) / 2 -> P = (3 - 1) / 2 = 1
    req_padding = 1
    
    padded_image = ConvolutionPaddingEngine.pad_image(raw_image, req_padding)
    assert padded_image.shape == (7, 7)
    
    # Ensure borders are absolute zero
    assert padded_image[0, 0] == 0.0
    assert padded_image[3, 3] == 1.0  # Internal pixel is untouched
    
    out_dimension = ConvolutionPaddingEngine.calculate_output_shape(i_size=5, f_size=3, stride=1, padding=1)
    assert out_dimension == 5  # Dimensions perfectly preserved
    
    print(f"[TASK 04 PASSED] Padding injected successfully. Spatial volume preserved at Output Shape: {out_dimension}")