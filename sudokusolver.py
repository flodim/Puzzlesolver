# /usr/bin/env python3

from typing import List, Optional, Iterator, Tuple, Iterable


class Sudoku:
    def __init__(self, size: int,
                matrix: List[List[int]]):

        self.size = size
        self.matrix = matrix

    @classmethod
    def from_file(cls, file_path: str, size: int) :
        file = open(file_path, "r")
        matrix = [[-1] * size for _ in range(size)]
        l=0
        for line in file:
            c=0
            for value in line.split(" "):
                try:
                    matrix[l][c] = int(value)
                except ValueError:

                    pass
                c+=1
            l+=1
        return cls(size, matrix)

def solve_forward_checking():
    #TODO: implement this
    return -1
def solve_heuristic():
    #TODO: implement this
    return -1





    def __str__(self) -> str:
        string=""
        l=0
        for line in self.matrix:
            c=0
            if l % 3 == 0:
                string+= "______________________________\n"
            for value in line:
                if  c % 3==0:
                    string += "|"
                if value != -1:
                    string += str(value) + '  '
                else:
                    string += '-  '
                c+=1
            string += '|\n'
            l+=1
        string += "______________________________"
        return string

if __name__ == '__main__':
    s = Sudoku.from_file('./sudoku.txt' , 9)
    print(s)



