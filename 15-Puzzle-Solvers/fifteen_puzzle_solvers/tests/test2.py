import heapq
import numpy as np
from prettytable import PrettyTable

class Puzzle15:
    def __init__(self, initial_state):
        self.initial_state = tuple(map(tuple, initial_state))  # Immutable state representation
        self.goal_state = ((1, 2, 3, 4),
                           (5, 6, 7, 8),
                           (9, 10, 11, 12),
                           (13, 14, 15, 0))  # Replace '#' with 0

    def manhattan_distance(self, state):
        total_distance = 0
        for i in range(4):
            for j in range(4):
                if state[i][j] != 0:  # Ignore empty tile
                    goal_pos = divmod(state[i][j] - 1, 4)
                    total_distance += abs(goal_pos[0] - i) + abs(goal_pos[1] - j)
        return total_distance

    def get_neighbors(self, state):
        neighbors = []
        state_arr = np.array(state, dtype=int)  # Ensure dtype is int
        x, y = np.where(state_arr == 0)
        x, y = int(x), int(y)
        moves = {"up": (x - 1, y), "down": (x + 1, y), "left": (x, y - 1), "right": (x, y + 1)}
        
        for move, (new_x, new_y) in moves.items():
            if 0 <= new_x < 4 and 0 <= new_y < 4:
                new_state = state_arr.copy()
                new_state[x, y], new_state[new_x, new_y] = new_state[new_x, new_y], new_state[x, y]
                neighbors.append((tuple(map(tuple, new_state)), move))
        
        return neighbors

    def format_state(self, state):
        return " | ".join([" ".join(map(str, row)) for row in state])

    def solve_a_star(self):
        open_set = []
        heapq.heappush(open_set, (self.manhattan_distance(self.initial_state), 0, self.initial_state, []))
        closed_set = set()
        
        table = PrettyTable()
        table.field_names = ["Step", "Open Set", "Closed Set", "Current State", "Children"]
        step = 0
        
        while open_set:
            step += 1
            _, cost, current_state, path = heapq.heappop(open_set)
            
            children = self.get_neighbors(current_state)
            table.add_row([
                step,
                " | ".join([self.format_state(state) for _, _, state, _ in open_set]),
                " | ".join([self.format_state(state) for state in closed_set]),
                self.format_state(current_state),
                " | ".join([self.format_state(child) for child, _ in children])
            ])
            
            if current_state == self.goal_state:
                print(table)
                return path  # Solution found
            
            closed_set.add(current_state)
            
            for neighbor, move in children:
                if neighbor not in closed_set:
                    heapq.heappush(open_set, (cost + 1 + self.manhattan_distance(neighbor), cost + 1, neighbor, path + [move]))
        
        print(table)
        return None  # No solution found

# Example usage
initial_state = [[1, 2, 3, 4],
                 [5, 6, 0, 8],  # Replace '#' with 0
                 [9, 10, 7, 12],
                 [13, 14, 11, 15]]

puzzle = Puzzle15(initial_state)
solution = puzzle.solve_a_star()
print("Solution:", solution)