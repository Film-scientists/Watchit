""" Unittests for testing start.py """

import unittest
import pandas as pd
from .. import start


class TestUserInteraction(unittest.TestCase):
    """
    Represent testing for start module
    """
    def test_ask_genres(self):
        """
        Test function ask_genres()
        """
        input_values = [1, 'Stop', 2, 'stop', 156, 'wd', 4, 5, 5, 'stop']
        output = []

        def mock_input(data):
            """ Overriding function input"""
            output.append(data)
            return input_values.pop(0)

        start.input = mock_input
        start.print = lambda s: output.append(s)

        result = {'Comedy', 'Action', 'Adventure', 'Children`s'}
        result_real = start.ask_genres()
        self.assertEqual(result, result_real)

    def test_ask_films(self):
        """
        Test function ask_films()
        """
        films_ser = pd.Series(['movie {}'.format(i) for i in range(1, 25)])
        input_values = ['4/5', 'stop', 'ee', 'Skip', 'skip', '6', '2', '3', '3.5', '3.0']
        input_values.extend(['5' for _ in range(17)])
        input_values.append('Stop')
        output = []

        def mock_input(_):
            """Overriding function input"""
            return input_values.pop(0)

        start.input = mock_input

        def mock_print(data):
            """Overriding function print"""
            lst_s = data.split(' ')
            output.append(lst_s[0])
            return data

        start.print = mock_print

        real_result = start.ask_ratings(films_ser)
        result_keys = ['movie {}'.format(i) for i in range(3, 24)]
        result_items = [2.0, 3.0, 3.5, 3.0]
        result_items.extend([5.0 for _ in range(17)])
        result = {result_keys[i]: result_items[i] for i in range(len(result_keys))}
        self.assertEqual(real_result, result)

        result_output = ['\nPlease,', '\nHow', 'movie', 'Please,', 'You',
                         'Please,', '\nHow', 'movie', '\nHow', 'movie', 'Please,']
        for _ in range(21):
            result_output.append('\nHow')
            result_output.append('movie')

        self.assertEqual(output, result_output)

    def test_filtering_films(self):
        """
        Tests function filter_films
        """
        user_fav_genres = {'Comedy', 'Romance'}
        movies_dataframe = pd.DataFrame.from_dict({'movieId': ['1', '2'],
                                                   'genres': ['Drama', 'Comedy']},
                                                  orient='columns')

        result_df = pd.DataFrame.from_dict({'movieId': [2],
                                            'genres': ['Comedy'],
                                            'number_fav_genres': [1]},
                                           orient='columns').reset_index(drop=True)

        real_result = start.filter_films(user_fav_genres, movies_dataframe).reset_index(drop=True)

        comparison = result_df == real_result
        columns = list(comparison)
        for i in columns:
            for j in range(len(comparison)):
                self.assertEqual(comparison[i][j], True)


def main():
    """
    Run tests for start.py
    """
    test = TestUserInteraction()
    test.test_ask_genres()
    print("test_ask_genres - passed")
    test.test_ask_films()
    print("test_ask_films - passed")
    test.test_filtering_films()
    print("test_filtering_films - passed")
