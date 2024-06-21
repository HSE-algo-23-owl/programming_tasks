import unittest
import numpy as np


class TestSimplexMethod(unittest.TestCase):
    def test_standard_maximization(self):
        c = np.array([3, 2])
        A = np.array([[1, 2], [2, 1]])
        b = np.array([8, 10])
        solution, objective = simplex_method(c, A, b)
        np.testing.assert_array_almost_equal(solution, [4, 2])
        self.assertAlmostEqual(objective, 16)

    def test_maximization_integer_coefficients(self):
        c = np.array([5, 4, 3])
        A = np.array([[2, 3, 1], [4, 1, 2], [3, 4, 2]])
        b = np.array([5, 11, 8])
        solution, objective = simplex_method(c, A, b)
        np.testing.assert_array_almost_equal(solution, [2, 0, 1])
        self.assertAlmostEqual(objective, 13)

    def test_maximization_equality_constraints(self):
        c = np.array([4, 6])
        A = np.array([[2, 3], [1, 1]])
        b = np.array([6, 3])
        solution, objective = simplex_method(c, A, b)
        np.testing.assert_array_almost_equal(solution, [0, 2])
        self.assertAlmostEqual(objective, 12)

    def test_unbounded_solution(self):
        c = np.array([1, 1])
        A = np.array([[-1, 1]])
        b = np.array([1])
        solution, objective = simplex_method(c, A, b)
        self.assertIsNone(solution)
        self.assertIsNone(objective)

    def test_no_feasible_solution(self):
        c = np.array([2, 3])
        A = np.array([[1, 1], [-1, -1]])
        b = np.array([2, -3])
        solution, objective = simplex_method(c, A, b)
        self.assertIsNone(solution)
        self.assertIsNone(objective)
        

if __name__ == '__main__':
    unittest.main()
