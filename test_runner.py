from unittest import TestSuite, TestLoader, TextTestRunner

from test.test_brute_force import TestBruteForce
from test.test_genetic_solver import TestGeneticSolver
from test.test_tournament import TestTournament
from test.tests_validate import TestValidate


def suite():
    """Создает набор тест-кейсов для тестирования модуля для решения задачи
    о рюкзаке."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestValidate))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestBruteForce))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestGeneticSolver))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestTournament))
    return test_suite


if __name__ == '__main__':
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
