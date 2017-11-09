from collections import deque
from typing import Tuple, Iterable, List, Reversible, Iterator
from sys import stdin
from io import StringIO


def int_sqrt(number: int):
    for i in range(number):
        if i*i == number:
            return i
        if i*i > number:
            return None
    return None


class PuzzleState:

    EMPTY = 0

    def __init__(self, pieces: Tuple, size: int, parent: 'PuzzleState'=None):
        self.pieces = pieces
        self.size = size
        self.parent = parent

    @classmethod
    def from_string(cls, pieces_str: str, parent: 'PuzzleState'=None) -> 'PuzzleState':
        pieces = tuple(map(int, pieces_str.split()))
        size = int_sqrt(len(pieces))

        if size is None:
            raise Exception("Invalid number of pieces (%d)" % len(pieces))

        return cls(pieces, size, parent)

    @classmethod
    def from_input(cls, file=stdin, parent=None):
        pieces_str = file.read()
        cls.from_string(pieces_str, parent)

    def is_solved(self) -> bool:
        if self.pieces[-1] != self.EMPTY:
            return False
        for index, value in enumerate(self.pieces[:-2]):
            if value > self.pieces[index + 1]:
                return False
        return True

    def empty_index(self) -> int:
        for index, value in enumerate(self.pieces):
            if value == self.EMPTY:
                return index
        raise Exception("Cannot find empty index.")

    def swap(self, index1: int, index2: int) -> 'PuzzleState':
        state_as_list = list(self.pieces)
        state_as_list[index1], state_as_list[index2] = state_as_list[index2], state_as_list[index1]
        return PuzzleState(tuple(state_as_list), self.size, self)

    def successors(self) -> Iterable['PuzzleState']:
        empty_index = self.empty_index()

        up_index = empty_index - self.size
        if up_index >= 0:
            yield self.swap(empty_index, up_index)

        down_index = empty_index + self.size
        if down_index < self.size * self.size:
            yield self.swap(empty_index, down_index)

        if empty_index % self.size != 0:
            left_index = empty_index - 1
            yield self.swap(empty_index, left_index)

        right_index = empty_index + 1
        if right_index % self.size != 0:
            yield self.swap(empty_index, right_index)

    def parents(self) -> Iterable['PuzzleState']:
        parent = self.parent
        while parent is not None:
            yield parent
            parent = parent.parent

    def history(self) -> Iterable['PuzzleState']:
        yield from reversed(list(self.parents()))
        yield self

    def __str__(self):
        with StringIO() as string:
            for i in range(0, len(self.pieces), self.size):
                print(*self.pieces[i:i+self.size], sep="\t", file=string)
            return string.getvalue()

    def __hash__(self):
        return self.pieces.__hash__()

    def __eq__(self, other):
        return self.pieces.__eq__(other.pieces)


class PuzzleSolverBase:

    @staticmethod
    def init_next_states(initial_state: PuzzleState):
        return deque([initial_state])

    @staticmethod
    def iter_next_states(next_states) -> Iterator[PuzzleState]:
        while True:
            try:
                yield next_states.popleft()
            except IndexError:
                break

    @staticmethod
    def add_next_state(next_states, state: PuzzleState):
        next_states.append(state)

    @classmethod
    def solve(cls, initial_state: PuzzleState) -> Iterable[PuzzleState]:

        next_states = cls.init_next_states(initial_state)
        visited_states = set()
        for state in cls.iter_next_states(next_states):
            visited_states.add(state)

            if state.is_solved():
                return state.history()

            successors = (s for s in state.successors()
                          if s not in visited_states)

            for successor in successors:
                cls.add_next_state(next_states, successor)
                visited_states.add(successor)

            # print("next states: %s" % len(next_states))
            # print("visited states: %s" % len(visited_states))
            # print("current depth: %s" % len(list(state.parents())))
            # print(state)


if __name__ == '__main__':

    puzzle_easy = PuzzleState((5, 4, 0,
                               6, 1, 8,
                               7, 3, 2), 3)

    puzzle_solved = PuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0), 3)
    puzzle_solved2 = PuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0), 3)

    solution = PuzzleSolverBase.solve(puzzle_easy)

    if solution:
        for i, state in enumerate(solution):
            print("Step %d:" % i)
            print(state)
    else:
        print("No solution found")

