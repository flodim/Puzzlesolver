from random import shuffle
from typing import List


class Puzzle:
    def __init__(self, size: int, values: List[int]):
        self.size = size
        self.nb_values = size*size
        self.matrix = [[]*size]
        for index, value in enumerate(values):
            line, column = divmod(index, size)
            self.matrix[line, column] = value

    @classmethod
    def from_random(cls, size):
        values = list(range(size))
        shuffle(values)
        return cls(size, values)

    def move(self, x: int, y: int, dx: int, dy: int):
        # TODO: implement this
        pass


    def solve(self):
        pass

    def is_correct(self, line, column):
        expected = line*self.size + column + 1
        return self.matrix[line][column] == expected

    def count_correct(self):
        correct_positions = 0
        for line in range(self.size):
            for column in range(self.size):
                if self.is_correct(line, column):
                    correct_positions += 1
        return correct_positions

    def manhattan(self, line, column):
        value = self.matrix[line][column]
        expected_line, expected_column = divmod(value-1, self.size)

