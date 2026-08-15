# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Generative Adversarial Network (GAN) Minimax Loss
Description: Computes the Zero-Sum Binary Cross Entropy loss evaluating the 
             Generator's ability to fool the Discriminator.
"""
import numpy as np  # type: ignore


class GANAdversarialEngine:
    @staticmethod
    def discriminator_loss(d_real_preds: np.ndarray, d_fake_preds: np.ndarray) -> float:
        # Discriminator maximizes log(D(x)) + log(1 - D(G(z)))
        # Using BCE Loss equivalent: True labels for real data (1), Fake labels for generated (0)
        eps = 1e-12
        loss_real = -np.mean(np.log(d_real_preds + eps))
        loss_fake = -np.mean(np.log(1.0 - d_fake_preds + eps))
        
        return float(loss_real + loss_fake)

    @staticmethod
    def generator_loss(d_fake_preds: np.ndarray) -> float:
        # Non-Saturating Heuristic: Generator maximizes log(D(G(z)))
        # Instead of minimizing log(1 - D(G(z))) which suffers from vanishing gradients
        eps = 1e-12
        # Generator wants Discriminator to predict 1 (Real) for its fake data
        loss_gen = -np.mean(np.log(d_fake_preds + eps))
        
        return float(loss_gen)


if __name__ == "__main__":
    # Discriminator predictions probabilities [0.0, 1.0]
    preds_on_real_data = np.array([0.9, 0.8, 0.95])  # D is confident these are real
    preds_on_fake_data = np.array([0.1, 0.2, 0.05])  # D is confident these are fake
    
    d_loss = GANAdversarialEngine.discriminator_loss(preds_on_real_data, preds_on_fake_data)
    g_loss = GANAdversarialEngine.generator_loss(preds_on_fake_data)
    
    # D is performing well, so D_loss should be low, and G_loss should be high
    assert d_loss < 0.5
    assert g_loss > 1.5
    
    print(f"[TASK 03 PASSED] GAN Minimax Loss computed. D_Loss: {d_loss:.4f} | G_Loss: {g_loss:.4f}")