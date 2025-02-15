from dataclasses import dataclass
from typing import List, Tuple
import heapq

@dataclass
class PuzzleState:
    board: List[List[int]]
    g_cost: int = 0
    parent = None
    
    def __lt__(self, other):
        return self.f_cost() < other.f_cost()
    
    def get_blank_position(self) -> Tuple[int, int]:
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return (-1, -1)
    
    def manhattan_distance(self) -> int:
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    value = self.board[i][j]
                    goal_i, goal_j = (value-1) // 3, (value-1) % 3
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance
    
    def f_cost(self) -> int:
        return self.g_cost + self.manhattan_distance()
    
    def get_moves(self) -> List['PuzzleState']:
        moves = []
        i, j = self.get_blank_position()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for di, dj in directions:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_board = [row[:] for row in self.board]
                new_board[i][j], new_board[new_i][new_j] = new_board[new_i][new_j], new_board[i][j]
                new_state = PuzzleState(new_board, self.g_cost + 1)
                new_state.parent = self
                moves.append(new_state)
        return moves
    
    def to_string_format(self) -> str:
        """Convert the board to the required string format with heuristic"""
        state_str = []
        for row in self.board:
            for elem in row:
                if elem == 0:
                    state_str.append('#')
                else:
                    state_str.append(str(elem))
        return f"[{''.join(state_str)}]{self.manhattan_distance()}"

def solve_puzzle(initial_state: PuzzleState):
    frontier = []
    heapq.heappush(frontier, initial_state)
    frontier_set = {str(initial_state.board)}
    closed_set = set()
    
    # Initialize table tracking
    table_entries = []
    
    # Add initial entry
    initial_entry = {
        'frontier': [initial_state.to_string_format()],
        'closed': [],
        'current': None,
        'children': []
    }
    table_entries.append(initial_entry)
    
    while frontier:
        current = heapq.heappop(frontier)
        frontier_set.remove(str(current.board))
        
        if current.board == [[1,2,3], [4,5,6], [7,8,0]]:
            return table_entries, current
        
        closed_set.add(str(current.board))
        moves = current.get_moves()
        
        # Track children before filtering
        all_children = [move.to_string_format() for move in moves]
        
        # Filter moves
        valid_moves = [
            move for move in moves
            if str(move.board) not in closed_set and str(move.board) not in frontier_set
        ]
        
        # Add valid moves to frontier
        for move in valid_moves:
            heapq.heappush(frontier, move)
            frontier_set.add(str(move.board))
        
        # Create table entry for this step
        entry = {
            'frontier': [state.to_string_format() for state in frontier],
            'closed': [current.to_string_format()],
            'current': current.to_string_format(),
            'children': all_children
        }
        table_entries.append(entry)
    
    return table_entries, None

def print_table(entries):
    print("-" * 120)
    print(f"{'Μέτωπο αναζήτησης':<40} {'Κλειστό σύνολο':<30} {'Τρέχουσα κατάσταση':<20} {'Παιδιά':<30}")
    print("-" * 120)
    
    for entry in entries:
        frontier = ', '.join(entry['frontier'])
        closed = '-' if not entry['closed'] else ', '.join(entry['closed'])
        current = '-' if entry['current'] is None else entry['current']
        children = ', '.join(entry['children'])
        
        # Truncate long strings
        if len(frontier) > 37: frontier = frontier[:34] + "..."
        if len(closed) > 27: closed = closed[:24] + "..."
        if len(children) > 27: children = children[:24] + "..."
        
        print(f"{frontier:<40} {closed:<30} {current:<20} {children:<30}")
    
    print("-" * 120)

def main():
    # Initial state from instructions
    initial_board = [[1, 2, 3], [4, 8, 5], [7, 6, 0]]
    initial_state = PuzzleState(initial_board)
    
    print("Initial state:")
    print(initial_state.to_string_format())
    
    table_entries, final_state = solve_puzzle(initial_state)
    
    if final_state:
        print("\nSolution found!")
        print_table(table_entries)
    else:
        print("\nNo solution found!")

if __name__ == "__main__":
    main()
