# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Exponential Learning Rate Decay Scheduler
Description: Dynamically curtails the optimizer step size over epochs, allowing
             broad exploration initially and fine-grained convergence at the end.
"""
import numpy as np  # type: ignore


class LearningRateScheduler:
    @staticmethod
    def exponential_decay(initial_lr: float, epoch: int, decay_rate: float) -> float:
        # lr_t = lr_0 * exp(-decay_rate * epoch)
        new_lr = initial_noise = initial_lr * np.exp(-decay_rate * epoch)
        return float(new_lr)

    @staticmethod
    def time_based_decay(initial_lr: float, epoch: int, decay_rate: float) -> float:
        # lr_t = lr_0 / (1 + decay_rate * epoch)
        new_lr = initial_lr / (1.0 + decay_rate * epoch)
        return float(new_lr)


if __name__ == "__main__":
    lr_base = 0.1
    rate = 0.05
    
    lr_epoch_0 = LearningRateScheduler.exponential_decay(lr_base, 0, rate)
    lr_epoch_10 = LearningRateScheduler.exponential_decay(lr_base, 10, rate)
    lr_epoch_50 = LearningRateScheduler.exponential_decay(lr_base, 50, rate)
    
    assert lr_epoch_0 == 0.1
    assert lr_epoch_10 < lr_epoch_0
    assert lr_epoch_50 < lr_epoch_10
    
    print(f"[TASK 05 PASSED] LR Schedulers evaluated. E0: {lr_epoch_0:.4f} -> E10: {lr_epoch_10:.4f} -> E50: {lr_epoch_50:.4f}")