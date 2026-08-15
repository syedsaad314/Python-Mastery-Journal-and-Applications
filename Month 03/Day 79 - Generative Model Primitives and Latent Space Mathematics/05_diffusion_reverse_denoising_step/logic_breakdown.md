# Logic Breakdown: Diffusion Reverse Step (Denoising)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
A trained Diffusion Model (like U-Net) doesn't output a clean image directly; it predicts the raw matrix of random noise ($\epsilon_\theta$) present in the current degraded image $x_t$. We must mathematically subtract this noise while preserving the stability of the probability distribution.

## My Approach
I implemented the reverse Markov step logic based on Langevin Dynamics. The engine cannot simply subtract the noise blindly. Instead, it scales the predicted noise by $\frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}}$ and deducts it to find the mean ($\mu_\theta$). Crucially, to prevent the sequence from collapsing deterministically, the algorithm *re-injects* a controlled, scaled amount of fresh variance ($\sigma_t z$) at every step (except $t=0$). This keeps the model exploring the latent distribution safely until convergence.

## Complexity Profile
* Runtime Bounds: $O(D)$ computing localized array math.
* Space Constraints: $O(D)$ intermediate allocation footprint for the variance stochasticity factor $z$.