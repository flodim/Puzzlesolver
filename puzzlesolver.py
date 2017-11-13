import heapq
from io import StringIO
from statistics import mean
from sys import stdin
from time import time
from typing import Tuple, Iterable, List


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
        min_index, max_index = (index1, index2) if index1 < index2 else (index2, index1)
        new_pieces = (*self.pieces[:min_index],
                      self.pieces[max_index],
                      *self.pieces[min_index+1:max_index],
                      self.pieces[min_index],
                      *self.pieces[max_index+1:])

        return PuzzleState(new_pieces, self.size, self)

    def successors(self) -> Iterable['PuzzleState']:
        empty_index = self.empty_index()

        if empty_index % self.size != 0:
            left_index = empty_index - 1
            yield self.swap(empty_index, left_index)

        down_index = empty_index + self.size
        if down_index < len(self.pieces):
            yield self.swap(empty_index, down_index)

        up_index = empty_index - self.size
        if up_index >= 0:
            yield self.swap(empty_index, up_index)

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

        for i, piece in enumerate(self.pieces[:-1]):
            if piece != i+1:
                nb_incorrect += 1

        if self.pieces[-1] != 0:
            nb_incorrect += 1

        return nb_incorrect

    def rowcol(self, index) -> Tuple[int, int]:
        return divmod(index, self.size)

    def expected_rowcol(self, piece):
        if piece == 0:
            expected_row = expected_col = self.size - 1
        else:
            expected_row, expected_col = self.rowcol(piece-1)
        return expected_row, expected_col

    def manhattan_sum(self) -> int:
        distance = 0
        for i, piece in enumerate(self.pieces):
            row, col = divmod(i, self.size)
            expected_row, expected_col = self.expected_rowcol(piece)
            distance += abs(col-expected_col) + abs(row-expected_row)
        return distance

    def __str__(self):
        with StringIO() as string:
            for i in range(0, len(self.pieces), self.size):
                print(*self.pieces[i:i+self.size], sep=",", file=string)
            return string.getvalue()

    def __hash__(self):
        return self.pieces.__hash__()

    def __eq__(self, other):
        return self.pieces.__eq__(other.pieces)


class PuzzleSolver:
    def __init__(self):
        self.iterations = 0

    def init_next_states(self, initial_state: PuzzleState) -> List[PuzzleState]:
        return [initial_state]

    def pop_state(self, next_states: List) -> PuzzleState:
        return next_states.pop()

    def add_next_state(self, next_states: List, state: PuzzleState):
        next_states.append(state)

    def iter_next_states(self, next_states) -> Iterable[PuzzleState]:
        self.iterations = 0
        while True:
            try:
                yield self.pop_state(next_states)
                self.iterations += 1
            except IndexError:
                break

    def clean(self):
        pass

    def solve(self, initial_state: PuzzleState) -> Iterable[PuzzleState]:
        next_states = self.init_next_states(initial_state)
        visited_states = set()
        for state in (self.iter_next_states(next_states)):
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
        super().__init__()
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
        return state.manhattan_sum()


class PuzzleSolverHybrid(PuzzleSolverCountCorrect):
    def get_state_weight(self, state: PuzzleState):
        return state.manhattan_sum() + state.count_incorrect()


def profile_solvers(solvers: Iterable[PuzzleSolver], puzzles : Iterable[PuzzleState]):
    for puzzle in puzzles:
        print(puzzle)
        for solver in solvers:
            start_time = time()
            solution = solver.solve(puzzle)
            end_time = time()

            print("Solver: %s" % solver.__class__.__name__)
            print("Size: %s" % puzzle.size)
            print("Solution steps: %s" % len(list(solution)) if solution else None)
            print("Iterations: %s" % solver.iterations)
            print("Duration: %s" % (end_time - start_time))


def profile_solvers_csv(solvers: Iterable[PuzzleSolver], puzzles : Iterable[PuzzleState], iterations_per_test: int):
    for puzzle in puzzles:
        print(puzzle)
        print("Solver name,Size,Solution steps,Iterations,Mean duration,Min duration,Max duration,Iterations per test")
        for solver in solvers:
            durations = []
            solution = None
            for n in range(iterations_per_test):
                start_time = time()
                solution = solver.solve(puzzle)
                end_time = time()
                durations.append(end_time - start_time)

            name = solver.__class__.__name__
            size = puzzle.size
            steps = len(list(solution)) if solution else None
            iterations = solver.iterations

            mean_duration = mean(durations)
            max_duration = max(durations)
            min_duration = min(durations)

            print(name, size, steps, iterations, mean_duration, min_duration, max_duration, iterations_per_test, sep=',')
        print()


if __name__ == '__main__':
    solvers = (
        PuzzleSolver(),
        PuzzleSolverCountCorrect(),
        PuzzleSolverManhattan(),
        PuzzleSolverHybrid(),
    )

    puzzles = (
        PuzzleState((5, 4, 0,
                     6, 1, 8,
                     7, 3, 2), 3),

        PuzzleState((2,  1,  3, 15,
                     7, 10,  4,  8,
                     14, 6, 13,  5,
                     11, 9, 12,  0), 4),

        PuzzleState((3,   7,   4, 10, 15,
                     0,   1,   5,  8, 20,
                     12,  2,  13,  9, 24,
                     6,   17,  21, 14, 23,
                     11,  18,  16, 19,  22), 5),

        PuzzleState((23,  3,  2,  8, 13,
                     24,  5,  1, 12, 10,
                     19,  9, 18, 15, 22,
                     11, 16,  7,  4, 17,
                     20, 14,  6, 21, 0), 5),

        PuzzleState((9,  4,  1,  21, 12, 10,
                     15, 11, 23, 8,  25, 18,
                     28, 7,  32, 0,  17, 27,
                     16, 13, 19, 29, 35, 6,
                     24, 20, 2,  30, 5,  3,
                     26, 22, 33, 14, 31, 34), 6),
    )

    profile_solvers_csv(solvers, puzzles, 10)
