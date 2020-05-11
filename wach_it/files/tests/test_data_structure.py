"""
Module with tests
"""
import unittest
import pandas as pd
from . import Saber
from ..data.test_only import ratings


class Tester(unittest.TestCase):
    """
    Represent module for testing Data Structure
    """
    def setUp(self):
        """
        Do the set-up
        """
        self.saber = Saber(ratings)
        self.data_frame = pd.read_csv(ratings)

    def test_avrg(self):
        """
        Test for average user rating
        """
        saber = self.saber
        d_f = self.data_frame
        for id_, frame in d_f.groupby("userId"):
            expected = round(frame["rating"].mean())
            real = saber[id_-1]
            self.assertEqual(real.av_r, expected)

    def test_weight(self):
        """
        Test for user weight
        """
        saber = self.saber
        d_f = self.data_frame
        for id_, _ in d_f.groupby("userId"):
            if id_ > 2:
                first = saber[id_ - 1].weighting(saber[id_ - 2])
                second = saber[id_ - 2].weighting(saber[id_ - 1])
                self.assertEqual(first, second)

    def test_repr(self):
        """
        Test for repr() and str() of user
        """
        saber = self.saber
        d_f = self.data_frame
        for id_, _ in d_f.groupby("userId"):
            real = saber[id_-1]
            self.assertTrue(str(real.av_r) in str(real))
            self.assertTrue(str(id_) in repr(real))

    def test_movies(self):
        """
        Test for functions that return movies
        """
        saber = self.saber
        d_f = self.data_frame
        for id_, frame in d_f.groupby("userId"):
            expected_movies = set(frame["movieId"])
            real_movies = saber[id_ - 1].get_movies()
            self.assertSetEqual(expected_movies, real_movies)
        all_movies_expected = set(d_f["movieId"].unique())
        all_movies_real = saber.all_movies()
        self.assertSetEqual(all_movies_expected, all_movies_real)

    def test_matrix(self):
        """
        Test for matrix generator
        """
        saber = self.saber
        d_f = self.data_frame
        saber.set_main(d_f[1:5])
        real = saber.matrix().T.drop(-1)
        expected = d_f.pivot(index='userId', columns='movieId', values='rating').fillna(0)
        self.assertEqual(real.shape, expected.shape)


def main():
    """
    Run tests for Saber class
    """
    test = Tester()
    test.setUp()
    test.test_avrg()
    print("average_test - passed")
    test.test_weight()
    print("user_weighting_test - passed")
    test.test_repr()
    print("representation_test - passed")
    test.test_movies()
    print("movies_test - passed")
    test.test_matrix()
    print("matrix_generation_test - passed")
