from fifteen_puzzle_solvers.services import PuzzleValidationService


class PuzzleSolver:
    """
    Executes different puzzle solver strategies (algorithms) and prints the solution and the performance
    """

    def __init__(self, strategy):
        self._strategy = strategy
        self.puzzle_validation_service = PuzzleValidationService()

    def run(self):
        if not self.puzzle_validation_service.is_solvable(self._strategy.start):
            raise RuntimeError('This puzzle is not solvable')
        self._strategy.solve_puzzle()

    def print_performance(self):
        print(f'{self._strategy} - Expanded Nodes: {self.get_num_expanded_nodes()}')

    def print_solution(self):
        print('Solution:')
        print(f'{"Step":<5} {"Current Search":<30} {"Closed Nodes":<30} {"Present Node":<20} {"Children":<30}')
        print('-' * 115)
        for step_num, (current_search, closed_nodes, present_node, children) in enumerate(self._strategy.search_info):
            current_search_str = ', '.join([str(node) for _, node in current_search])
            closed_nodes_str = ', '.join([str(node) for node in closed_nodes])
            children_str = ', '.join([str(child) for child in children])
            print(f'{step_num + 1:<5} {current_search_str:<30} {closed_nodes_str:<30} {str(present_node):<20} {children_str:<30}')
            print('-' * 115)

    def get_num_expanded_nodes(self):
        return self._strategy.num_expanded_nodes

    def get_solution(self):
        return self._strategy.solution

    def stop(self):
        if hasattr(self._strategy, 'stop'):
            self._strategy.stop()