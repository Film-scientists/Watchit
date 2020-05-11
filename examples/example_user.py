"""
Module for examples of usage User ADT and Saber ADT.
"""
import pandas as pd
from data_structure import User, Saber


RATINGS = pd.read_csv('ratings_1M.csv')
del RATINGS['timestamp']
RATINGS = RATINGS.loc[RATINGS['userId'] <= 653]


def example_user(ratings):
    user1 = User(541, ratings)
    user2 = User(653, ratings)

    av_rate1 = user1.get_average_rating(ratings)
    norm_rate1 = user1.normalize_ratings(ratings)

    weight = user1.weighting(user2)

    print('Average rating of user 541 is: {}\n'
          'Normalized ratings for user 541: {}\n'
          'Weight of user 653 for user 541: {}\n'.format(av_rate1, norm_rate1, weight))


if __name__ == "__main__":
    example_user(RATINGS)