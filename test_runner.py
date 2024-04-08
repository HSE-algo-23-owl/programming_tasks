from unittest import TestSuite, TestLoader, TextTestRunner


from schedule_pack.tests.test_task import TestTask
from schedule_pack.tests.test_schedule_item import TestScheduleItem
from schedule_pack.tests.test_schedule import TestSchedule
from schedule_pack.tests.test_staged_task import TestStagedTask
from schedule_pack.tests.test_conveyor_schedule import TestConveyorSchedule


def suite():
    """Создает набор тест-кейсов для тестирования модуля Расписания."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestTask))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestScheduleItem))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestSchedule))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestStagedTask))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestConveyorSchedule))
    return test_suite


if __name__ == '__main__':
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
