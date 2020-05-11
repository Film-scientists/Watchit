"""
Module for examples of usage User ADT and Saber ADT.
"""
import pandas as pd
from data_structure import User, Saber


RATINGS = pd.read_csv('ratings_1M.csv')
del RATINGS['timestamp']
RATINGS_NEEDED = RATINGS.loc[RATINGS['userId'] <= 653]
RATINGS_USER1 = RATINGS_NEEDED.loc[RATINGS_NEEDED['userId'] <= 541]
RATINGS_USER2 = RATINGS_NEEDED.loc[RATINGS_NEEDED['userId'] > 541]


def example_user(ratings1, ratings2):
    user1 = User(541, ratings1)
    user2 = User(653, ratings2)

    av_rate1 = user1.get_average_rating(ratings1)
    av_rate2 = user2.get_average_rating(ratings2)
    norm_rate1 = user1.normalize_ratings(ratings1)

    weight = user1.weighting(user2)

    print('Average rating of user 541 is: {}\n'
          'Normalized ratings for user 541: {}\n'
          'Weight of user 653 for user 541: {}\n'.format(av_rate1, norm_rate1, weight))
    print('Average rating of user 653 is: {}'.format(av_rate2))


def example_saber(filename, ratings):
    sab = Saber(filename)
    sab.set_main(ratings)
    matrix = sab.matrix()
    print('Matrix for user 541: \n', matrix)


if __name__ == "__main__":
    example_user(RATINGS_USER1, RATINGS_USER2)
    example_saber('ratings_1M.csv', RATINGS_USER1)