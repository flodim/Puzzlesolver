#/usr/bin/env python3
from random import shuffle
from typing import List, Optional, IO
from io import StringIO

class Puzzle:
    def __init__(self, size: int, values: List[int]):
        self.size = size
        self.nb_values = size*size - 1
        self.matrix = [[-1]*size for _ in range(size)]
        for index, value in enumerate(values):
            line, column = divmod(index, size)
            self.matrix[line][column] = value
            if value == 0:
                self.empty_line = line
                self.empty_column = column

    @classmethod
    def from_random(cls, size):
        values = list(range(size*size))
        shuffle(values)
        return cls(size, values)

    @classmethod
    def from_keyboard(cls):
        size = int(input('enter matrix size: '))
        values = list(range(size))
        for i in range(0, size*size):
            values[i] = int(input("enter value "+str(i)+": "))
        return cls(size, values)

    def move(self, dx: int, dy: int):
        target_line = self.empty_line+dy
        target_column = self.empty_column+dx
        target_value = self.matrix[target_line][target_column]
        self.matrix[target_line][target_column] = 0
        self.matrix[self.empty_line][self.empty_column] = target_value
        self.empty_line = target_line
        self.empty_column = target_column

    def move_up(self):
        self.move(0, -1)

    def move_down(self):
        self.move(0, 1)

    def move_left(self):
        self.move(-1, 0)

    def move_right(self):
        self.move(1, 0)

    def solve(self):
        pass

    def play(self):
        while not self.is_solved:
            self.print()
            key = input('Direction ?')
            try:
                if key in ['w', 'k', 'up']:
                    self.move_up()
                elif key in ['s', 'j', 'down']:
                    self.move_down()
                elif key in ['a', 'h', 'left']:
                    self.move_left()
                elif key in ['d', 'l', 'right']:
                    self.move_right()
                else:
                    print("Unknown direction")
            except IndexError:
                print('This direction is out of bounds')

    def print(self, file: Optional[IO[str]] = None):
            print('-' * (self.size*4 - 1), file=file)
            for line in self.matrix:
                print(*line, sep='\t', file=file)
            print('-' * (self.size*4 - 1), file=file)

    def __str__(self):
        with StringIO() as f:
            self.print(file=f)
            return f.getvalue()

    def cell_is_correct(self, line, column):
        expected = line*self.size + column + 1
        return self.matrix[line][column] == expected

    def count_correct(self):
        correct_positions = 0
        for line in range(self.size):
            for column in range(self.size):
                if self.cell_is_correct(line, column):
                    correct_positions += 1
        return correct_positions

    @property
    def is_solved(self):
        return self.count_correct() == self.nb_values

    def manhattan_distance(self, line: int, column: int):
        value = self.matrix[line][column]
        expected_line, expected_column = divmod(value-1, self.size)
        v_distance = abs(line-expected_line)
        h_distance = abs(column-expected_column)
        return v_distance, h_distance


if __name__ == '__main__':
    puzzle = Puzzle.from_random(3)
    puzzle.play()
