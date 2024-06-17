import unittest
from main import a_star_search, GridWithWeights


class TestAStarAlgorithm(unittest.TestCase):

    def test_small_map_no_obstacles(self):
        grid = GridWithWeights(3, 3)
        start, goal = (0, 0), (2, 2)
        expected_path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
        self.assertEqual(a_star_search(grid, start, goal), expected_path)

    def test_medium_map_some_obstacles(self):
        grid = GridWithWeights(5, 5)
        grid.walls = [(2, 2), (1, 2)]
        start, goal = (0, 0), (4, 4)
        path = a_star_search(grid, start, goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)

    def test_large_map_dense_obstacles(self):
        grid = GridWithWeights(10, 10)
        grid.walls = [(i, j) for i in range(10) for j in range(10) if
                      (i + j) % 3 == 0 and (i, j) not in [(0, 0), (9, 9)]]
        start, goal = (0, 0), (9, 9)
        path = a_star_search(grid, start, goal)
        if path is not None:
            self.assertEqual(path[0], start)
            self.assertEqual(path[-1], goal)
        else:
            self.assertIsNone(path)

    def test_start_outside_bounds(self):
        grid = GridWithWeights(5, 5)
        start, goal = (6, 6), (4, 4)
        with self.assertRaises(ValueError):
            a_star_search(grid, start, goal)

    def test_goal_outside_bounds(self):
        grid = GridWithWeights(5, 5)
        start, goal = (0, 0), (6, 6)
        with self.assertRaises(ValueError):
            a_star_search(grid, start, goal)

    def test_dense_obstacles_with_narrow_paths(self):
        grid = GridWithWeights(5, 5)
        grid.walls = [(1, 0), (1, 1), (1, 3), (1, 4), (3, 0), (3, 1), (3, 3), (3, 4)]
        start, goal = (0, 0), (4, 4)
        expected_path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4)]
        self.assertEqual(a_star_search(grid, start, goal), expected_path)

    def test_no_path_exists(self):
        grid = GridWithWeights(5, 5)
        grid.walls = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4)]
        start, goal = (0, 0), (4, 4)
        self.assertIsNone(a_star_search(grid, start, goal))

    def test_large_map_sparse_obstacles(self):
        grid = GridWithWeights(10, 10)
        grid.walls = [(i, j) for i in range(10) for j in range(10) if (i + j) % 5 == 0]
        start, goal = (0, 0), (9, 9)
        with self.assertRaises(ValueError) as context:
            path = a_star_search(grid, start, goal)

        self.assertTrue("Start or goal is on an obstacle." in str(context.exception))

    def test_large_map_no_obstacles(self):
        grid = GridWithWeights(10, 10)
        start, goal = (0, 0), (9, 9)
        path = a_star_search(grid, start, goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)

    def test_invalid_start_goal_format(self):
        grid = GridWithWeights(5, 5)
        with self.assertRaises(ValueError):
            a_star_search(grid, "start", (4, 4))

    def test_invalid_start_goal_length(self):
        grid = GridWithWeights(5, 5)
        with self.assertRaises(ValueError):
            a_star_search(grid, (0,), (4, 4))

    def test_start_or_goal_on_obstacle(self):
        grid = GridWithWeights(5, 5)
        grid.walls = [(0, 0), (4, 4)]
        with self.assertRaises(ValueError):
            a_star_search(grid, (0, 0), (4, 4))


if __name__ == '__main__':
    unittest.main()
