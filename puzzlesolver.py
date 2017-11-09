from abc import ABC, abstractstaticmethod, abstractmethod
from collections import deque
from time import time
from typing import Tuple, Iterable, List, Reversible, Iterator
from sys import stdin
from io import StringIO
import heapq


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

    def count_incorrect(self) -> int:
        nb_incorrect = 0
        last_i = len(self.pieces) - 1
        for i, piece in enumerate(self.pieces):
            if piece != i+1 or (piece == 0 and i != last_i):
                nb_incorrect += 1
        return nb_incorrect

    def manhattan(self) -> int:
        distance = 0

        for i, piece in enumerate(self.pieces):
            col = i % self.size
            row = i // self.size
            if piece == 0:
                expected_col = self.size - 1
                expected_row = expected_col
            else:
                expected_col = piece-1 % self.size
                expected_row = piece-1 // self.size

            distance += abs(col-expected_col) + abs(row-expected_row)
        return distance

    def __str__(self):
        with StringIO() as string:
            for i in range(0, len(self.pieces), self.size):
                print(*self.pieces[i:i+self.size], sep="\t", file=string)
            return string.getvalue()

    def __hash__(self):
        return self.pieces.__hash__()

    def __eq__(self, other):
        return self.pieces.__eq__(other.pieces)


class PuzzleSolver:

    def init_next_states(self, initial_state: PuzzleState) -> List[PuzzleState]:
        return [initial_state]

    def pop_state(self, next_states: List) -> PuzzleState:
        return next_states.pop()

    def add_next_state(self, next_states: List, state: PuzzleState):
        next_states.append(state)

    def iter_next_states(self, next_states) -> Iterable[PuzzleState]:
        while True:
            try:
                yield self.pop_state(next_states)
            except IndexError:
                break

    def clean(self):
        pass

    def solve(self, initial_state: PuzzleState) -> Iterable[PuzzleState]:
        next_states = self.init_next_states(initial_state)
        visited_states = set()
        for state in self.iter_next_states(next_states):
            visited_states.add(state)

            if state.is_solved():
                return state.history()

            successors = (s for s in state.successors()
                          if s not in visited_states)

            for successor in successors:
                self.add_next_state(next_states, successor)
                visited_states.add(successor)
        self.clean()


class PuzzleSolverCountCorrect(PuzzleSolver):

    def __init__(self):
        self.push_count = 0

    def get_state_weight(self, state: PuzzleState) -> int:
        return state.count_incorrect()

    def init_next_states(self, initial_state: PuzzleState) -> List[Tuple[int, int, PuzzleState]]:
        next_states = [(self.get_state_weight(initial_state), self.push_count, initial_state)]
        heapq.heapify(next_states)
        self.push_count = 1
        return next_states

    def pop_state(self, next_states: List[Tuple[int, int, PuzzleState]]) -> PuzzleState:
        return heapq.heappop(next_states)[2]

    def add_next_state(self, next_states: List[Tuple[int, int, PuzzleState]], state: PuzzleState):
        heapq.heappush(next_states, (self.get_state_weight(state), self.push_count, state))
        self.push_count += 1

    def clean(self):
        self.push_count = 0


class PuzzleSolverManhattan(PuzzleSolverCountCorrect):
    def get_state_weight(self, state: PuzzleState):
        return state.manhattan()


def test_solver(solver: PuzzleSolver):
    puzzle = PuzzleState((5, 4, 0,
                          6, 1, 8,
                          7, 3, 2), 3)

    start_time = time()
    solution = solver.solve(puzzle)
    end_time = time()

    print("Solver: %s" % solver.__class__.__name__)
    print("Steps: %s" % len(list(solution)) if solution else "not solved")
    print("Duration: %s" % (end_time - start_time))
    print()


def test_solvers(*solvers: PuzzleSolver):
    for solver in solvers:
        test_solver(solver)


if __name__ == '__main__':
    test_solvers(
        PuzzleSolver(),
        PuzzleSolverCountCorrect(),
        PuzzleSolverManhattan()
    )
