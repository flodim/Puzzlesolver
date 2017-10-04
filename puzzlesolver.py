# /usr/bin/env python3
from collections import deque
from copy import deepcopy
from random import shuffle
from typing import List, Optional, Iterator, Tuple, Iterable

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class PuzzleState:
    def __init__(
            self, size: int,
            matrix: List[List[int]],
            empty_line: int,
            empty_column: int,
            last_move=None,
            last_state=None):

        self.size = size
        self.nb_values = size * size - 1
        self.matrix = matrix
        self.empty_line = empty_line
        self.empty_column = empty_column
        self.last_move = last_move
        self.last_state = last_state

    @classmethod
    def from_iterable(cls, size: int, values: Iterable[int]) -> 'PuzzleState':
        empty_line = None
        empty_column = None
        matrix = [[-1] * size for _ in range(size)]
        for index, value in enumerate(values):
            line, column = divmod(index, size)
            matrix[line][column] = value
            if value == 0:
                empty_line = line
                empty_column = column
        return cls(size, matrix, empty_line, empty_column)

    @classmethod
    def from_random(cls, size: int) -> 'PuzzleState':
        values = list(range(size * size))
        shuffle(values)
        return cls.from_iterable(size, values)

    @classmethod
    def from_keyboard(cls) -> 'PuzzleState':
        size = int(input('enter matrix size: '))
        values = list(range(size))
        for i in range(0, size * size):
            values[i] = int(input("enter value " + str(i) + ": "))
        return cls.from_iterable(size, values)

    @property
    def values(self) -> Tuple:
        values = tuple([self.matrix[l][c] for l, c in self.matrix_indices])
        return tuple(values)

    @property
    def successors(self) -> List['PuzzleState']:
        return [self.move(direction)
                for direction in [UP, DOWN, LEFT, RIGHT]
                if self.can_move(direction)]

    @property
    def matrix_indices(self) -> Iterator[Tuple[int, int]]:
        return ((line, column)
                for line in range(self.size)
                for column in range(self.size))

    @property
    def nb_correct(self) -> int:
        correct_cells = sum(1 for l, c in self.matrix_indices
                            if self.cell_is_correct(l, c))
        return correct_cells

    @property
    def is_solved(self) -> bool:
        return self.nb_correct == self.nb_values

    @property
    def path(self) -> List['PuzzleState']:
        inverted_path = [self]
        current = self
        while current.last_state is not None:
            inverted_path.append(current.last_state)
            current = current.last_state
        return list(reversed(inverted_path))

    @property
    def total_manhattan_distance(self) -> int:
        distances = (self.manhattan_distance(l, c)
                     for l, c in self.matrix_indices)
        total = sum(distances)
        return total

    def __str__(self) -> str:
        string = "----------\n"
        for line in self.matrix:
            for value in line:
                string += str(value) + '\t'
            string += '\n'
        string += "----------"
        return string

    def __eq__(self, other: 'PuzzleState') -> bool:
        return self.size == other.size and self.__hash__() == other.__hash__()

    def __hash__(self) -> int:
        return hash(self.values)

    def cell_is_correct(self, line: int, column: int) -> bool:
        expected = line * self.size + column + 1
        return self.matrix[line][column] == expected

    def can_move(self, direction: Tuple[int, int]) -> bool:
        if direction == self.last_move:
            return False
        if direction == UP:
            return self.empty_line > 0
        if direction == DOWN:
            return self.empty_line < self.size - 1
        if direction == LEFT:
            return self.empty_column > 0
        if direction == RIGHT:
            return self.empty_column < self.size - 1

    def manhattan_distance(self, line: int, column: int) -> int:
        value = self.matrix[line][column]
        expected_line, expected_column = divmod(value - 1, self.size)
        v_distance = abs(line - expected_line)
        h_distance = abs(column - expected_column)
        distance = v_distance + h_distance
        return distance

    def move(self, direction: Tuple(int, int)) -> 'PuzzleState':
        dx, dy = direction
        target_line = self.empty_line + dy
        target_column = self.empty_column + dx
        target_value = self.matrix[target_line][target_column]
        new_matrix = deepcopy(self.matrix)
        new_matrix[target_line][target_column] = 0
        new_matrix[self.empty_line][self.empty_column] = target_value
        new_empty_line = target_line
        new_empty_column = target_column
        return PuzzleState(self.size, new_matrix, new_empty_line, new_empty_column, direction, self)


def solve(initial_puzzle: PuzzleState) -> Optional[List[PuzzleState]]:
    if initial_puzzle.is_solved:
        return [initial_puzzle]

    queue = deque([initial_puzzle])
    old_states = set()

    while True:
        try:
            current_state = queue.pop()
        except IndexError:
            return None

        for successor in current_state.successors:
            if successor.is_solved:
                return successor.path
            if successor not in old_states:
                queue.append(successor)
        old_states.add(current_state)


if __name__ == '__main__':
    puzzle = PuzzleState.from_iterable(3, [5, 4, 0, 6, 1, 8, 7, 3, 2])
    solution = solve(puzzle)

    if solution:
        print("Solved in %d steps" % len(solution))
        for state in solution:
            print(state)
    else:
        print("Unsolvable")
