import unittest


from main import hello


class TestHello(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), 'Hello world!')


if __name__ == '__main__':
    unittest.main()
