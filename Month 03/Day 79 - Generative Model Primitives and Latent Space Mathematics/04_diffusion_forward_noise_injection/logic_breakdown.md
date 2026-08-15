# Logic Breakdown: Diffusion Forward Process (Closed-Form)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Diffusion Models destroy images sequentially over 1,000 discrete timesteps ($x_0 \rightarrow x_1 \dots \rightarrow x_{1000}$) to create training data. Running a 1,000-step loop for every image in a massive dataset during training generates insurmountable computational delays.

## My Approach
I utilized the **Closed-Form Reparameterization** property of Markov Chains. Because the sum of normally distributed variables remains normally distributed, we can mathematically bypass the iterative loop entirely. By taking the cumulative product of the noise schedule variances ($\bar{\alpha}_t$), the network instantly projects the original image $x_0$ to any arbitrary timestep $x_t$ in a single $O(1)$ scalar multiplication matrix operation: $x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$.

## Complexity Profile
* Runtime Bounds: $O(1)$ relative to timesteps; computes instantly directly at arbitrary $t$.
* Space Constraints: $O(M)$ allocated to hold the singular injected Gaussian noise matrix $\epsilon$.