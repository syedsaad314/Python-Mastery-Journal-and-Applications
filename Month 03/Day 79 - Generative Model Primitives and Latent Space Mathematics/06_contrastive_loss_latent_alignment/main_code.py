# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: InfoNCE Contrastive Loss (CLIP Primitive)
Description: Aligns dual-modal embeddings (e.g., Image and Text vectors) by 
             maximizing cosine similarity of positive pairs via scaled Softmax.
"""
import numpy as np  # type: ignore


class ContrastiveLearningEngine:
    @staticmethod
    def compute_infonce_loss(image_embeddings: np.ndarray, text_embeddings: np.ndarray, temperature: float = 0.07) -> float:
        # 1. L2 Normalize the vectors so dot products directly equal Cosine Similarity
        img_norm = image_embeddings / np.linalg.norm(image_embeddings, axis=1, keepdims=True)
        txt_norm = text_embeddings / np.linalg.norm(text_embeddings, axis=1, keepdims=True)
        
        # 2. Compute Cosine Similarity Matrix (Logits)
        # Shape: (batch_size, batch_size)
        logits = np.dot(img_norm, txt_norm.T)
        
        # 3. Scale by temperature
        logits_scaled = logits / temperature
        
        # 4. The target labels are the diagonal indices (Image i matches Text i)
        batch_size = logits.shape[0]
        labels = np.arange(batch_size)
        
        # 5. Compute Cross Entropy Loss in both directions
        # Image-to-Text
        exp_i = np.exp(logits_scaled - np.max(logits_scaled, axis=1, keepdims=True))
        probs_i = exp_i / np.sum(exp_i, axis=1, keepdims=True)
        loss_i = -np.mean(np.log(probs_i[np.arange(batch_size), labels] + 1e-9))
        
        # Text-to-Image
        exp_t = np.exp(logits_scaled.T - np.max(logits_scaled.T, axis=1, keepdims=True))
        probs_t = exp_t / np.sum(exp_t, axis=1, keepdims=True)
        loss_t = -np.mean(np.log(probs_t[np.arange(batch_size), labels] + 1e-9))
        
        # Symmetric InfoNCE loss
        return (loss_i + loss_t) / 2.0


if __name__ == "__main__":
    np.random.seed(42)
    
    # 3 perfectly aligned pairs (Loss should be extremely low)
    ideal_imgs = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    ideal_txts = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    
    # 3 mismatched pairs
    bad_imgs = np.random.randn(3, 2)
    bad_txts = np.random.randn(3, 2)
    
    ideal_loss = ContrastiveLearningEngine.compute_infonce_loss(ideal_imgs, ideal_txts)
    bad_loss = ContrastiveLearningEngine.compute_infonce_loss(bad_imgs, bad_txts)
    
    assert ideal_loss < bad_loss
    
    print(f"[TASK 06 PASSED] Contrastive InfoNCE Loss computed. Ideal Pairs: {ideal_loss:.4f} | Mismatched: {bad_loss:.4f}")