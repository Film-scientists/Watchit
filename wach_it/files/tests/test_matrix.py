"""
Module with tests
"""
import unittest
import pandas as pd
from ..matrix import matrix_fct
from ..data_structure import Saber
from ..data.test_only import ratings, test as test_f, movies as movies_f


PRED = 200


class TesterMatrix(unittest.TestCase):
    """
    Represent tester for matrix algorithm
    """
    def setUp(self):
        """
        Do the set-up
        """
        self.saber = Saber(ratings)
        data = pd.read_csv(test_f).sort_values(by="rating")
        self.training = data[-50:]
        self.saber.set_main(data[:-50])
        self.movies = pd.read_csv(movies_f)

    def test_result_m(self):
        """
        Test for result of algorithm
        """
        saber = self.saber
        movies = self.movies
        res = matrix_fct(saber, movies, PRED).drop("genres", axis=1)
        intersection = res.merge(self.training, how="left", on="movieId").dropna()
        self.assertTrue(not intersection.empty)


def main():
    """
    Run tests matrix.py
    """
    test = TesterMatrix()
    test.setUp()
    test.test_result_m()
    print("result_of_algorithm_test - passed")
