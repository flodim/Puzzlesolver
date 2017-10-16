# /usr/bin/env python3

from typing import List, Optional, Iterator, Tuple, Iterable

import math


class Sudoku:
    def __init__(self, size: int,
                 matrix: List[List[int]]):

        self.size = size
        self.matrix = matrix

    @classmethod
    def from_file(cls, file_path: str, size: int):
        file = open(file_path, "r")
        matrix = [[-1] * (size) for _ in range(size)]
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

    def __str__(self) -> str:
        string = ""
        space = "  "
        long_line = " ___________________________________\n"
        sub_array_size = math.sqrt(self.size)
        l = 0
        for line in self.matrix:
            c = 0
            if l % sub_array_size == 0:
                string += long_line
            for value in line:
                if c % sub_array_size == 0:
                    string += "|" + space
                string += str(value) + space if value != -1 else '-' + space
                c += 1
            string += '|\n'
            l += 1
        string += long_line
        return string


def solve_forward_checking():
    # TODO: implement this
    return -1


def solve_heuristic():
    # TODO: implement this
    return -1


if __name__ == '__main__':
    s = Sudoku.from_file('./sudoku.txt', 9)
    print(s)
