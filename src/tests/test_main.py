import unittest
from src.main import print_hi


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_print_hi_with_string(self):
        self.assertEqual("Hi, good", print_hi("good"))


if __name__ == "__main__":
    unittest.main()
