"""
CORE CONCEPT: Optimization via Vanilla Gradient Descent
Building an iterative gradient evaluation simulator tracking step adjustments across
convex loss functions. Deconstructs the core continuous optimization engine that drives 
supervised model adjustments in modern AI.
"""

from typing import Callable

def simulate_gradient_descent(
    objective_function: Callable[[float], float],
    derivative_function: Callable[[float], float],
    initial_position: float,
    learning_rate: float = 0.1,
    max_iterations: int = 100,
    tolerance: float = 1e-6
) -> float:
    """Iteratively minimizes a function using directional partial derivatives."""
    current_position = initial_position
    
    for _ in range(max_iterations):
        gradient = derivative_function(current_position)
        
        # Determine movement down the slope
        next_position = current_position - (learning_rate * gradient)
        
        # Assess convergence threshold boundary
        if abs(next_position - current_position) < tolerance:
            break
            
            
        current_position = next_position
        
    return current_position


if __name__ == "__main__":
    # Minimizing f(x) = x^2. The true analytical global minimum resides at x = 0.
    f_x = lambda x: x ** 2
    df_x = lambda x: 2 * x
    
    minimized_solution = simulate_gradient_descent(f_x, df_x, initial_position=8.0)
    print(f"Optimizer Convergence Location: {minimized_solution}")