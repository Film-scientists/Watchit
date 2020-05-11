"""
Module with tests
"""
import unittest
from .. import recomendation_engine


PRED = 100


class Tester(unittest.TestCase):
    """
    Represent testing for recommendation engine
    """
    def test_result(self):
        """
        Test for correct type of output
        """
        recomendation_engine.print = lambda arg: arg
        self.assertTrue(isinstance(recomendation_engine.core(True), list))


def main():
    """
    Run tests recomendation_engine.py
    """
    test = Tester()
    test.test_result()
    print("test_for_output_of_rec_eng - passed")
