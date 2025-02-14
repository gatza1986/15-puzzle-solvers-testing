from fifteen_puzzle_solvers.domain.puzzle import Puzzle
from fifteen_puzzle_solvers.services.puzzle import PuzzleHeuristicService, PuzzleValidationService
from fifteen_puzzle_solvers.services.algorithms import AStar
from fifteen_puzzle_solvers.services.solver import PuzzleSolver
import time


class AStarTracker(AStar):
    def __init__(self, puzzle, heuristic=None):
        super().__init__(puzzle, heuristic)
        self.frontier_history = []
        self.closed_history = []
        self.current_history = []
        self.children_history = []
        
    def solve(self):
        # Initialize with start state
        self.frontier_history.append([str(self.initial_puzzle)])
        self.closed_history.append([])
        self.current_history.append(None)
        self.children_history.append([])
        
        return super().solve(track_steps=True)
    
    def step(self, current, expanded_nodes):
        # Store the current state before processing
        current_str = str(current)
        frontier_str = [str(node) for node in self.frontier]
        closed_str = [str(node) for node in self.closed_list]
        
        # Let the parent class process the step
        children = super().step(current, expanded_nodes)
        
        # Store the children after processing
        children_str = [str(child) for child in children]
        
        # Update tracking history
        self.current_history.append(current_str)
        self.frontier_history.append(frontier_str)
        self.closed_history.append(closed_str)
        self.children_history.append(children_str)
        
        return children
    
    def print_search_table(self):
        print("\n" + "-" * 120)
        print(f"{'Μέτωπο αναζήτησης':<40} {'Κλειστό σύνολο':<30} {'Τρέχουσα κατάσταση':<20} {'Παιδιά':<30}")
        print("-" * 120)
        
        for i in range(len(self.current_history)):
            # Handle initial state
            if i == 0:
                print(f"{str(self.frontier_history[i]):<40} {str(self.closed_history[i]):<30} {'-':<20} {str(self.children_history[i]):<30}")
                continue
                
            current = self.current_history[i]
            
            # Format lists for display
            frontier = str(self.frontier_history[i])
            closed = str(self.closed_history[i])
            children = str(self.children_history[i])
            
            # Truncate long lists for display
            if len(frontier) > 37:
                frontier = frontier[:34] + "..."
            if len(closed) > 27:
                closed = closed[:24] + "..."
            if len(children) > 27:
                children = children[:24] + "..."
                
            print(f"{frontier:<40} {closed:<30} {current:<20} {children:<30}")
        
        print("-" * 120)


def format_position(position):
    """Helper function to format position for display"""
    flat_position = []
    for row in position:
        for elem in row:
            if elem == 0:
                flat_position.append('#')
            else:
                flat_position.append(str(elem))
    return ''.join(flat_position)


def main():
    # Test with different initial states for 3x3 puzzle
    test_cases_3x3 = [
        [[1, 2, 3], [4, 5, 6], [7, 8, 0]],  # Already solved
        [[1, 2, 3], [4, 5, 0], [7, 8, 6]],  # Easy
        [[1, 2, 3], [4, 0, 5], [7, 8, 6]],  # Medium
        [[1, 0, 2], [4, 5, 3], [7, 8, 6]],  # Another medium
        [[0, 1, 2], [4, 5, 3], [7, 8, 6]],  # Harder
        [[5, 1, 3], [4, 0, 2], [7, 8, 6]],  # More difficult
    ]
    
    # Test with different initial states for 4x4 puzzle
    test_cases_4x4 = [
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]],  # Already solved
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0], [13, 14, 15, 12]],  # Easy
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 0, 10, 11], [13, 14, 15, 12]],  # Medium
        [[1, 2, 3, 0], [5, 6, 7, 4], [9, 10, 11, 8], [13, 14, 15, 12]],  # Another medium
        [[0, 1, 2, 3], [5, 6, 7, 4], [9, 10, 11, 8], [13, 14, 15, 12]],  # Harder
    ]
    
    # Choose which test cases to run (3x3 or 4x4)
    test_cases = test_cases_3x3
    size = 3
    
    for i, initial_state in enumerate(test_cases):
        print(f"\nTest Case {i+1}")
        print(f"Initial state: {initial_state}")
        
        # Create puzzle
        puzzle = Puzzle(initial_state)
        
        # Create tracker and solve
        tracker = AStarTracker(puzzle)
        solver = PuzzleSolver(tracker)
        
        start_time = time.time()
        solver.run()
        end_time = time.time()
        
        # Print results
        print(f"Solution found in {end_time - start_time:.4f} seconds")
        
        # Get solution
        solution = solver.get_solution()
        if solution:
            print(f"Solution cost: {len(solution) - 1}")
            
            # Print search table
            tracker.print_search_table()
            
            # Print solution path
            print("\nSolution path:")
            for step, p in enumerate(solution):
                print(f"Step {step}: {format_position(p.position)}")
        else:
            print("No solution found")


if __name__ == "__main__":
    main()