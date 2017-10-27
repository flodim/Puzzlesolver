# /usr/bin/env python3

from typing import List, Optional, Iterator, Tuple, Iterable

import math

EMPTY = -1


def check_row():
    return 0


class Sudoku:
    def __init__(self, size: int,
                 matrix: List[List[int]]):

        self.size = size
        self.matrix = matrix
        self.block_size = int(math.sqrt(size))

    @classmethod
    def from_file(cls, file_path: str, size: int):
        file = open(file_path, "r")
        matrix = [[-1] * size for _ in range(size)]
        l = 0
        for line in file:
            c = 0
            for value in line.split(" "):
                try:
                    matrix[l][c] = int(value)
                except ValueError:
                    # do nothing
                    pass
                c += 1
            l += 1
        return cls(size, matrix)

    @property
    def empty_squares(self) -> List[Tuple[int, int]]:
        empty_squares = []
        for row in range(self.size):
            for col in range(self.size):
                if self.matrix[row][col] == EMPTY:
                    empty_squares.append([row, col])
        return empty_squares

    def solve_heuristic(self) -> bool:
        # TODO: implement this
        return False

    def solve_forward_checking(self) -> bool:
        return False;

    def solve_backtracking(self) -> bool:
        if len(self.empty_squares) == 0:
            return True
        possible_values = list(range(1, 10))
        square=self.empty_squares[0]
        row = square[0]
        col = square[1]
        while len(possible_values) != 0:
            value = possible_values[0]
            possible_values.remove(value)
            if self.check_column(value, row) and \
                    self.check_row(value, col) and\
                    self.check_block(value,square):
                self.matrix[row][col] = value
                if self.solve_backtracking():
                    return True
                else:
                    self.matrix[row][col] = EMPTY
        return False

    def check_column(self, value: int, row: int) -> bool:
        for col in range(self.size):
            if self.matrix[row][col] == value:
                return False
        return True

    def check_row(self, value: int, col: int) -> bool:
        for row in range(self.size):
            if self.matrix[row][col] == value:
                return False
        return True

    def check_block(self, value, square: Tuple[int, int]) -> bool:
        row= square[0]-(square[0]%self.block_size);
        col = square[1] - (square[1] % self.block_size);

        for i in range(row,row+(self.block_size)):
            for j in range(col,col+(self.block_size)):
                if self.matrix[i][j] == value:
                    return False
        return True

    def __str__(self) -> str:
        string = ""
        space = "  "
        long_line = "-------------------------------------\n"
        l = 0
        for line in self.matrix:
            c = 0
            if l % self.block_size == 0:
                string += long_line
            for value in line:
                if c % self.block_size == 0:
                    string += "|" + space
                string += str(value) + space if value != EMPTY else '-' + space
                c += 1
            string += '|\n'
            l += 1
        string += long_line
        return string


if __name__ == '__main__':
    s = Sudoku.from_file('./sudoku.txt', 9)
    print(s)
    s.solve_backtracking()
    print("solve backtracking:\n")
    print(s)
