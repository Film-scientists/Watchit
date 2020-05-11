"""
Some config
"""
import pathlib
CONFIG = str(pathlib.Path(__file__).parent.absolute())

final = CONFIG + "/final_ratings_2.csv"
movies = CONFIG + "/movies.csv"
ratings = CONFIG + "/ratings_1M.csv"
users = CONFIG + "/users.txt"
