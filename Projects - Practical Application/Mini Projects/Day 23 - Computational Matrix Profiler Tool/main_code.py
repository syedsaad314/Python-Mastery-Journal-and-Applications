"""
System: Computational Matrix Profiler Tool
Description: A performance benchmarking framework designed to map out execution footprints 
             and processing durations across mathematical grid mutations.
Lead Engineer: Syed Saad Bin Irfan
"""

import sys
import time
from typing import List, Dict, Any

class ComputationalMatrixProfilerTool:
    """Evaluates memory footprint metrics and processing speeds across mathematical array grids."""
    
    @staticmethod
    def generate_unrolled_matrix(dimension_size: int) -> List[List[int]]:
        """Generates a standard nested grid matrix array using inline list comprehension tools."""
        return [[column * 2 for column in range(dimension_size)] for row in range(dimension_size)]

    @staticmethod
    def transform_matrix_elements(matrix_grid: List[List[int]]) -> List[List[int]]:
        """Mutates elements inside the matrix array, tracking execution performance profiles."""
        # Multiplies each matrix entry using an optimized list comprehension loop
        return [[element * 3 for element in data_row] for data_row in matrix_grid]

    def execute_profile_benchmark(self, operational_dimension: int) -> Dict[str, Any]:
        """Measures execution speed and memory allocations for matrix generation and transformation workloads."""
        metrics_payload: Dict[str, Any] = {}
        
        # Benchmark generation speed
        start_time = time.perf_counter()
        target_grid = self.generate_unrolled_matrix(operational_dimension)
        generation_duration = time.perf_counter() - start_time
        
        # Calculate raw space allocation requirements
        grid_memory_cost = sys.getsizeof(target_grid)
        for single_row in target_grid:
            grid_memory_cost += sys.getsizeof(single_row)
            
        # Benchmark transformation performance
        start_time = time.perf_counter()
        transformed_grid = self.transform_matrix_elements(target_grid)
        transformation_duration = time.perf_counter() - start_time
        
        # Populate profiling metrics log
        metrics_payload["matrix_dimensions"] = f"{operational_dimension}x{operational_dimension}"
        metrics_payload["generation_time_sec"] = round(generation_duration, 5)
        metrics_payload["transformation_time_sec"] = round(transformation_duration, 5)
        metrics_payload["calculated_memory_allocated_bytes"] = grid_memory_cost
        
        return metrics_payload


if __name__ == "__main__":
    print("\n=== INITIALIZING COMPUTATIONAL MATRIX PROFILER ENGINE ===\n")
    
    profiler_instance = ComputationalMatrixProfilerTool()
    target_dimension = 600  # Creates a 600x600 data matrix grid
    
    print(f"[PROFILER] Executing grid processing cycles for dimension: {target_dimension}...")
    execution_insights = profiler_instance.execute_profile_benchmark(target_dimension)
    
    print("\n=== MATRIX METRICS BENCHMARK EVALUATION ===")
    for metric_key, metric_value in execution_insights.items():
        print(f" {metric_key.replace('_', ' ').title():<36}: {metric_value}")
    print("=" * 46)