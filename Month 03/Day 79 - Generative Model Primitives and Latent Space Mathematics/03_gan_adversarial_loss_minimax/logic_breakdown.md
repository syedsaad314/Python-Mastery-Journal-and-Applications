# Logic Breakdown: GAN Adversarial Minimax Loss
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Generative models historically minimized static loss functions (like MSE), causing blurry output because the model averages all possibilities. We need an objective function that mathematically forces the generation of highly realistic, sharp synthetic data.

## My Approach
I implemented the GAN Minimax objective. The network is split into two competing agents. 
The Discriminator evaluates Binary Cross Entropy to separate real and fake images. 
The Generator completely ignores real data; its sole objective function is evaluated based purely on the Discriminator's predictions of the fake data. If the Discriminator is fooled (predicts `1.0`), the Generator loss approaches zero. This forces a zero-sum mathematical game where the Generator must continually invent sharper features to beat an ever-improving Discriminator.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution calculating bounded vectorized logarithms.
* Space Constraints: $O(N)$ memory required for holding evaluation matrices to calculate adversarial gradients.