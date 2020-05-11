"""
Some config
"""
import pathlib
CONFIG = str(pathlib.Path(__file__).parent.absolute())

ratings = CONFIG + "/ratings_test.csv"
movies = CONFIG + "/movies_test.csv"
test = CONFIG + "/test.csv"
