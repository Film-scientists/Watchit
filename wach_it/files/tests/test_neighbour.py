"""
Module with tests
"""
import unittest
import pandas as pd
from ..neighbour import nearest_n
from ..data_structure import Saber
from ..data.test_only import test as test_f, ratings, movies as movies_f


PRED = 100


class TesterNeighbour(unittest.TestCase):
    """
    Represent tester for nearest neighbour algorithm
    """
    def setUp(self):
        """
        Do the set-up
        """
        self.saber = Saber(ratings)
        data = pd.read_csv(test_f).sort_values(by="rating")
        self.training = data[-10:]
        self.saber.set_main(data[:-10])
        self.movies = pd.read_csv(movies_f)

    def test_result_n(self):
        """
        Test for results of algorithm
        """
        saber = self.saber
        movies = self.movies
        res = nearest_n(movies, saber, PRED).drop("genres", axis=1)
        intersection = res.merge(self.training, how="left", on="movieId").dropna()
        self.assertTrue(not intersection.empty)


def main():
    """
    Run tests for neighbour.py
    """
    test = TesterNeighbour()
    test.setUp()
    test.test_result_n()
    print("result_of_algorithm_test - passed")
