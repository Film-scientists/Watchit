"""
Test all modules
"""
import unittest
from files.tests import test_data_structure, \
    test_matrix, \
    test_auth, \
    test_neighbour, \
    test_recomendation_engine, \
    test_start


class Test(unittest.TestCase):
    """
    Represent tester
    """

    @staticmethod
    def test_ds():
        """
        Test Data Structure
        """
        print(f"\n-----------Test Data Structure------------")
        test_data_structure.main()
        print(f"--------Passed Test Data Structure--------\n")

    @staticmethod
    def test_matrix_alg():
        """
        Test MATRIX Algorithm
        """
        print(f"\n-----------Test Matrix Algorithm------------")
        test_matrix.main()
        print(f"--------Passed Test Matrix Algorithm--------\n")

    @staticmethod
    def test_neighbour_alg():
        """
        Test NEAREST_NEIGHBOUR Algorithm
        """
        print(f"\n-----------Test Neighbour Algorithm------------")
        test_neighbour.main()
        print(f"--------Passed Test Neighbour Algorithm--------\n")

    @staticmethod
    def test_auth():
        """
        Test auth module
        """
        print(f"\n-------------------Test Auth-------------------")
        test_auth.main()
        print(f"----------------Passed Test Auth----------------\n")

    @staticmethod
    def test_rec():
        """
        Test recommendation_engine.py module
        """
        print(f"\n-----------Test Recommendation Engine-----------")
        test_recomendation_engine.main()
        print(f"-------Passed Test Recommendation Engine--------\n")

    @staticmethod
    def test_start():
        """
        Test start.py module
        """
        print(f"\n---------------Test Start Module----------------")
        test_start.main()
        print(f"------------Passed Test Start Module------------\n")


if __name__ == "__main__":
    unittest.main()
