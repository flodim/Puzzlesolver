import unittest

from puzzlesolver import Puzzle


class PuzzleTests(unittest.TestCase):
    def test_init(self):
        for size in range(2, 100):
            values = list(range(size*size))
            puzzle = Puzzle(size, values)
            puzzle_values = [value for line in puzzle.matrix for value in line]
            self.assertEqual(puzzle.size, size)
            self.assertListEqual(puzzle_values, values)

    def test_move(self):
        puzzle = Puzzle(3, [0, 1, 2,
                            3, 4, 5,
                            6, 7, 8])
        puzzle.move_right()
        self.assertListEqual(puzzle.matrix,
                             [[1, 0, 2],
                              [3, 4, 5],
                              [6, 7, 8]])
        puzzle.move_down()
        self.assertListEqual(puzzle.matrix,
                             [[1, 4, 2],
                              [3, 0, 5],
                              [6, 7, 8]])
        puzzle.move_left()
        self.assertListEqual(puzzle.matrix,
                             [[1, 4, 2],
                              [0, 3, 5],
                              [6, 7, 8]])
        puzzle.move_up()
        self.assertListEqual(puzzle.matrix,
                             [[0, 4, 2],
                              [1, 3, 5],
                              [6, 7, 8]])


if __name__ == '__main__':
    unittest.main()
