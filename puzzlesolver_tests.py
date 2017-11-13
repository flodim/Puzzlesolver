from unittest import TestCase

from puzzlesolver import PuzzleState


class TestPuzzleState(TestCase):

    def test_count_incorrect(self):
        state = PuzzleState((
            1, 2, 3,
            4, 5, 6,
            7, 8, 0), 3)
        self.assertEqual(state.count_incorrect(), 0)

        state = PuzzleState((
            1, 2, 3,
            4, 5, 0,
            7, 8, 6), 3)
        self.assertEqual(state.count_incorrect(), 2)

        state = PuzzleState((
            1, 2, 0,
            4, 5, 3,
            7, 8, 6), 3)
        self.assertEqual(state.count_incorrect(), 3)

        state = PuzzleState((
            1, 0, 2,
            4, 5, 3,
            7, 8, 6), 3)
        self.assertEqual(state.count_incorrect(), 4)

    def test_manhattan(self):
        state = PuzzleState((
            1, 2, 3,
            4, 5, 6,
            7, 8, 0), 3)
        self.assertEqual(state.manhattan_sum(), 0)

        state = PuzzleState((
            1, 2, 3,
            4, 5, 0,
            7, 8, 6), 3)
        self.assertEqual(state.manhattan_sum(), 2)

        state = PuzzleState((
            1, 2, 3,
            4, 0, 5,
            7, 8, 6), 3)
        self.assertEqual(state.manhattan_sum(), 4)
