# /usr/bin/env python3
from time import *
from timeit import Timer
from typing import List, Tuple

import math

from random import randint

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
        self.first_backtracking = True
        self.nb_assignment_before_backtracking = 0

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
            for value in range(1, self.size + 1):
                if self.check_row(value, col) and \
                        self.check_column(value, row) and \
                        self.check_block(value, (row, col)):
                    possible_values[row][col].append(value)
        return possible_values

    @property
    def most_constrained_squares(self) -> List[Tuple[int, int]]:
        squares = {i: [] for i in range(0, self.size + 1)}
        possible_values = self.possible_values
        for row, col in self.empty_squares:
            squares[len(possible_values[row][col])].append((row, col))
        return [square
                for i in range(1, self.size + 1)
                for square in squares[i]]

    @property
    def most_constrained_square(self) -> Tuple[int, int]:
        return self.most_constrained_squares[0]

    def solve_heuristic(self) -> bool:
        self.nb_recursive_call += 1
        nb_empty_squares = len(self.empty_squares)
        if nb_empty_squares == 0:
            return True
        possible_values = self.possible_values
        most_constrained_squares = self.most_constrained_squares

        # check that the sudoku is always solvable
        impossible_values = nb_empty_squares - len(most_constrained_squares)
        if impossible_values != 0:
            return False

        row, col = most_constrained_squares[0]
        values = possible_values[row][col]
        for value in values:
            self.matrix[row][col] = value
            self.nb_assignment_before_backtracking += 1 if self.first_backtracking else 0
            if self.solve_heuristic():
                return True
            else:
                self.matrix[row][col] = EMPTY
                self.first_backtracking = False
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
            self.matrix[row][col] = value
            if self.solve_forward_checking():
                return True
            else:
                self.matrix[row][col] = EMPTY
        return False

    def solve_backtracking(self) -> bool:
        self.nb_recursive_call += 1
        if len(self.empty_squares) == 0:
            return True
        values = list(range(1, self.size + 1))
        square = self.empty_squares[0]
        row = square[0]
        col = square[1]
        while len(values) != 0:
            value = values[0]
            values.remove(value)

            if self.check_column(value, row) and \
                    self.check_row(value, col) and \
                    self.check_block(value, square):
                self.matrix[row][col] = value
                self.nb_assignment_before_backtracking += 1 if self.first_backtracking else 0
                if self.solve_backtracking():
                    return True
                else:
                    self.matrix[row][col] = EMPTY
                    self.first_backtracking = False
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
        long_line=""
        for x in range((self.block_size*4+3)*self.block_size +1):
            long_line += "-"
        long_line += "\n"
        ln = 0
        for line in self.matrix:
            cl = 0
            if ln % self.block_size == 0:
                string += long_line
            for value in line:
                if cl % self.block_size == 0:
                    string += "|" + space
                if value != EMPTY:
                    if value < 10:
                        string += '0' + str(value) + space
                    else:
                        string += str(value) + space
                else:
                    string += '--' + space
                cl += 1
            string += '|\n'
            ln += 1
        string += long_line
        return string


def print_statistics(result: bool, nb_recursive_call: int, nb_assignment_before_backtracking: int, execution_time: float):
    if result:
        print("solved with a total of " + str(nb_recursive_call) + " recursive calls and "
              + str(nb_assignment_before_backtracking) + " assignment before first backtracking \n"
              + "this operation take " + str(execution_time) + " seconds.\n"
              )
    else:
        print("unsolvable\n")


if __name__ == '__main__':
    file = "./sudoku.txt"
    size = 9

    s = Sudoku.from_file(size, file)
    print("Unsolved sudoku:")
    print(s)
    print("=========== solve backtracking ===========\n")
    t0 = perf_counter()
    result = s.solve_backtracking()
    t1 = perf_counter()
    print_statistics(result, s.nb_recursive_call, s.nb_assignment_before_backtracking, t1 - t0)

    s = Sudoku.from_file(size, file)
    print("=========== solve heuristic ===========\n")
    print("first most constrained square: " + str(s.most_constrained_square))
    t0 = perf_counter()
    result = s.solve_heuristic()
    t1 = perf_counter()

    print_statistics(result, s.nb_recursive_call, s.nb_assignment_before_backtracking, t1 - t0)
