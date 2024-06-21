import numpy as np
from typing import Tuple, Optional


class SimplexSolver:
    def __init__(self, c: np.ndarray, A: np.ndarray, b: np.ndarray, maximize: bool = True):
        self.c = c if maximize else -c
        self.A = A
        self.b = b
        self.maximize = maximize
        self.m, self.n = A.shape
        self.basic_vars = list(range(self.n, self.n + self.m))
        self.tableau = self._create_tableau()

    def _create_tableau(self) -> np.ndarray:
        tableau = np.zeros((self.m + 1, self.n + self.m + 1))
        tableau[:-1, :self.n] = self.A
        tableau[:-1, self.n:-1] = np.eye(self.m)
        tableau[:-1, -1] = self.b
        tableau[-1, :self.n] = -self.c
        return tableau

    def _pivot(self, row: int, col: int) -> None:
        self.tableau[row] /= self.tableau[row, col]
        for i in range(self.tableau.shape[0]):
            if i != row:
                self.tableau[i] -= self.tableau[i, col] * self.tableau[row]
        self.basic_vars[row] = col

    def solve(self) -> Tuple[Optional[np.ndarray], Optional[float]]:
        iterations = 0
        max_iterations = 1000

        while np.any(self.tableau[-1, :-1] < -1e-10) and iterations < max_iterations:
            pivot_col = np.argmin(self.tableau[-1, :-1])
            ratios = np.where(self.tableau[:-1, pivot_col] > 1e-10,
                              self.tableau[:-1, -1] / self.tableau[:-1, pivot_col],
                              np.inf)
            if np.all(ratios == np.inf):
                return None, None
            pivot_row = np.argmin(ratios)
            self._pivot(pivot_row, pivot_col)
            iterations += 1

        if iterations == max_iterations:
            return None, None

        if np.any(self.tableau[:-1, -1] < -1e-10):
            return None, None

        solution = np.zeros(self.n)
        for i, var in enumerate(self.basic_vars):
            if var < self.n:
                solution[var] = self.tableau[i, -1]
        objective_value = self.tableau[-1, -1] * (-1 if not self.maximize else 1)
        return solution, objective_value

def simplex_method(c: np.ndarray, A: np.ndarray, b: np.ndarray, maximize: bool = True) -> Tuple[Optional[np.ndarray], Optional[float]]:
    solver = SimplexSolver(c, A, b, maximize)
    return solver.solve()


def main():
    c = np.array([3, 2])  # коэффициенты целевой функции
    A = np.array([[1, 2], [2, 1]])  # матрица коэффициентов ограничений
    b = np.array([8, 10])

    print(f"Максимизировать: {c[0]}x1 + {c[1]}x2")
    print(f"При ограничениях:")
    print(f"{A[0, 0]}x1 + {A[0, 1]}x2 <= {b[0]}")
    print(f"{A[1, 0]}x1 + {A[1, 1]}x2 <= {b[1]}")
    print("x1, x2 >= 0")

    solution, objective = simplex_method(c, A, b)

    if solution is not None and objective is not None:
        print("\nРешение:")
        print(f"x1 = {solution[0]:.2f}")
        print(f"x2 = {solution[1]:.2f}")
        print(f"Максимальное значение целевой функции: {objective:.2f}")
    else:
        print("\nЗадача не имеет решения или решение неограничено.")


if __name__ == '__main__':
    main()
