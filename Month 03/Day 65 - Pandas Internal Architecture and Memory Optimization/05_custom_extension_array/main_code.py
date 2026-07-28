# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: NumExpr Kernel Expressions via pd.eval
Description: Evaluates compound boolean and mathematical DataFrame expressions
             using C-compiled NumExpr kernels to prevent temporary array allocations.
"""
import numpy as np # pyright: ignore[reportMissingImports]
import pandas as pd # type: ignore


class NumExprAccelerationEngine:
    @staticmethod
    def evaluate_complex_filter(df: pd.DataFrame, threshold_a: float, threshold_b: float) -> pd.Series:
        # Avoids allocating multiple intermediate boolean mask arrays in memory
        expression = "(val_a > @threshold_a) & (val_b < @threshold_b)"
        return df.eval(expression, engine='numexpr')


if __name__ == "__main__":
    np.random.seed(42)
    n_rows = 5000
    df_data = pd.DataFrame({
        "val_a": np.random.randn(n_rows),
        "val_b": np.random.randn(n_rows)
    })
    
    mask_eval = NumExprAccelerationEngine.evaluate_complex_filter(df_data, threshold_a=0.5, threshold_b=0.0)
    
    # Standard python evaluation for assertions
    mask_standard = (df_data["val_a"] > 0.5) & (df_data["val_b"] < 0.0)
    assert pd.Series.equals(mask_eval, mask_standard)
    
    print(f"[TASK 04 PASSED] NumExpr kernel expression matched standard filter across {n_rows} rows.")