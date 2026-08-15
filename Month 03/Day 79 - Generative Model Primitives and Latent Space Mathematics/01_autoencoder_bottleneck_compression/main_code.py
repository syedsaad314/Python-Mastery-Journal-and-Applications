# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Autoencoder Bottleneck Compression
Description: Maps high-dimensional input into a compressed lower-dimensional latent 
             space, forcing the network to extract only the most critical features.
"""
import numpy as np  # type: ignore


class AutoencoderPrimitive:
    def __init__(self, input_dim: int, latent_dim: int):
        np.random.seed(42)
        # Encoder weights
        self.W_enc = np.random.randn(input_dim, latent_dim) * 0.1
        # Decoder weights
        self.W_dec = np.random.randn(latent_dim, input_dim) * 0.1

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        # 1. Encode into bottleneck (Linear projection)
        latent_vector = np.dot(x, self.W_enc)
        
        # 2. Decode back to original dimension
        reconstructed = np.dot(latent_vector, self.W_dec)
        
        return latent_vector, reconstructed

    @staticmethod
    def reconstruction_loss(x_original: np.ndarray, x_reconstructed: np.ndarray) -> float:
        # Mean Squared Error (MSE) measures information loss
        return float(np.mean(np.square(x_original - x_reconstructed)))


if __name__ == "__main__":
    # 5 samples of 100-dimensional data
    X = np.random.randn(5, 100)
    
    # Compress 100 dimensions down to 10
    ae = AutoencoderPrimitive(input_dim=100, latent_dim=10)
    
    z_latent, X_hat = ae.forward(X)
    
    # Assert physical dimensional compression and reconstruction
    assert z_latent.shape == (5, 10)
    assert X_hat.shape == (5, 100)
    
    loss = AutoencoderPrimitive.reconstruction_loss(X, X_hat)
    assert loss > 0.0
    
    print(f"[TASK 01 PASSED] Data compressed to latent bottleneck and reconstructed. MSE Loss: {loss:.4f}")