from fifteen_puzzle_solvers.domain.puzzle import Puzzle
from fifteen_puzzle_solvers.services.puzzle import PuzzleHeuristicService, PuzzleShuffleService, PuzzleValidationService
from fifteen_puzzle_solvers.services.algorithms import AStar, BreadthFirst
from fifteen_puzzle_solvers.services.solver import PuzzleSolver
from fifteen_puzzle_solvers.services.puzzle.constants import HEURISTIC_MANHATTAN_DISTANCE, HEURISTIC_MISPLACED

# Create an initial puzzle
initial_puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]])

# Run A* with Manhattan heuristic
astar_manhattan = AStar(initial_puzzle, heuristic=HEURISTIC_MANHATTAN_DISTANCE)
solver_manhattan = PuzzleSolver(astar_manhattan)
solver_manhattan.run()
print("A* with Manhattan Heuristic:")
solver_manhattan.print_solution()
solver_manhattan.print_performance()

# Run A* with Misplaced heuristic
astar_misplaced = AStar(initial_puzzle, heuristic=HEURISTIC_MISPLACED)
solver_misplaced = PuzzleSolver(astar_misplaced)
solver_misplaced.run()
print("\nA* with Misplaced Heuristic:")
solver_misplaced.print_solution()
solver_misplaced.print_performance()

# Run Breadth-First Search
breadth_first = BreadthFirst(initial_puzzle)
solver_breadth_first = PuzzleSolver(breadth_first)
solver_breadth_first.run()
print("\nBreadth-First Search:")
solver_breadth_first.print_solution()
solver_breadth_first.print_performance()
