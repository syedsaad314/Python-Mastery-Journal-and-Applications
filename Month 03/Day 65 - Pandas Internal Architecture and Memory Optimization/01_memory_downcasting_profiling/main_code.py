# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Automated DataFrame Memory Downcasting
Description: Reduces DataFrame memory footprint by downcasting numerical dtypes 
             to minimal subtype bounds and converting low-cardinality strings to categories.
"""
import sys
import numpy as np # type: ignore
import pandas as pd # type: ignore


class MemoryOptimizerEngine:
    @staticmethod
    def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        df_optimized = df.copy()
        
        # Optimize Integer columns
        for col in df_optimized.select_dtypes(include=['int64', 'int32']).columns:
            col_min = df_optimized[col].min()
            col_max = df_optimized[col].max()
            df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
            
        # Optimize Float columns
        for col in df_optimized.select_dtypes(include=['float64']).columns:
            df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
            
        # Optimize Object/String columns via Categorical encoding
        for col in df_optimized.select_dtypes(include=['object']).columns:
            num_unique = df_optimized[col].nunique()
            num_total = len(df_optimized[col])
            if num_unique / num_total < 0.5:  # Convert if cardinality < 50%
                df_optimized[col] = df_optimized[col].astype('category')
                
        return df_optimized


if __name__ == "__main__":
    raw_data = {
        "status_code": np.array([200, 404, 500, 200, 200] * 200, dtype=np.int64),
        "latency_ms": np.array([12.5, 98.1, 150.2, 11.0, 14.2] * 200, dtype=np.float64),
        "region": ["us-east-1", "eu-west-1", "us-east-1", "us-east-1", "eu-west-1"] * 200
    }
    df_raw = pd.DataFrame(raw_data)
    initial_mem = df_raw.memory_usage(deep=True).sum()
    
    df_opt = MemoryOptimizerEngine.optimize_dataframe(df_raw)
    final_mem = df_opt.memory_usage(deep=True).sum()
    
    assert df_opt["status_code"].dtype == np.int16 or df_opt["status_code"].dtype == np.int8
    assert df_opt["latency_ms"].dtype == np.float32
    assert isinstance(df_opt["region"].dtype, pd.CategoricalDtype)
    assert final_mem < initial_mem
    
    reduction_pct = (1 - (final_mem / initial_mem)) * 100
    print(f"[TASK 01 PASSED] Memory optimized from {initial_mem} to {final_mem} bytes ({reduction_pct:.2f}% reduction).")