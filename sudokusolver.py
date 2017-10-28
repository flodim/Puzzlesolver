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
        self.nb_recursive_call = 0

    @classmethod
    def from_file(cls, size: int, file_path: str):
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

    @property
    def possible_values(self) -> List[List[List[int]]]:
        possible_values = [[[] for x in range(self.size)] for y in range(self.size)]
        for empty_square in self.empty_squares:
            row = empty_square[0]
            col = empty_square[1]
            for value in range(1, 10):
                if self.check_row(value, col) and \
                        self.check_column(value, row) and \
                        self.check_block(value, (row, col)):
                    possible_values[row][col].append(value)
        return possible_values

    def solve_heuristic(self) -> bool:
        # TODO: implement this
        return False

    def solve_forward_checking(self) -> bool:
        self.nb_recursive_call += 1
        if len(self.empty_squares) == 0:
            return True
        square = self.empty_squares[0]
        row = square[0]
        col = square[1]
        values = self.possible_values[row][col]
        while len(values) != 0:
            value = values[0]
            values.remove(value)
            if self.forward_check(value,row,col):
                self.matrix[row][col] = value
                if self.solve_forward_checking():
                    return True
                else:
                    self.matrix[row][col] = EMPTY
        return False

    def forward_check(self, value: int, cur_row:int, cur_col: int) -> bool:
        for row in range(self.size):
            if row == cur_row:
                continue
            for col in range(self.size):
                if cur_col == cur_col:
                    continue
                if len(self.possible_values[row][col]) == 1 and self.possible_values[row][col][0] == value:
                    return False
        return True

    def solve_backtracking(self) -> bool:
        self.nb_recursive_call += 1
        if len(self.empty_squares) == 0:
            return True
        possible_values = list(range(1, 10))
        square = self.empty_squares[0]
        row = square[0]
        col = square[1]
        while len(possible_values) != 0:
            value = possible_values[0]
            possible_values.remove(value)
            if self.check_column(value, row) and \
                    self.check_row(value, col) and \
                    self.check_block(value, square):
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

    def check_block(self, value: int, square: Tuple[int, int]) -> bool:
        row = square[0] - (square[0] % self.block_size)
        col = square[1] - (square[1] % self.block_size)

        for i in range(row, row + self.block_size):
            for j in range(col, col + self.block_size):
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
    s = Sudoku.from_file(9, './sudoku.txt')
    print(s)
    print("solve forward checking:\n")
    s.solve_forward_checking()
    print(s)
    print("solved with " + str(s.nb_recursive_call) + " recursive calls")
