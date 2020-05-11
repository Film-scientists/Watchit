"""
Chatting module
"""

import pandas as pd
from .data import final


def filter_films(user_genres, d_f):
    """
    (set, Dataframe) -> (Dataframe)
    Return dataframe with films of
    user`s favourite genres.
    """
    d_f['movieId'] = d_f.apply(lambda x: bool(set(x["genres"].split("|")) & user_genres) *
                                         x["movieId"] or None, axis=1)
    d_f.dropna(inplace=True)
    d_f['movieId'] = d_f['movieId'].astype(int)

    d_f['number_fav_genres'] = d_f.apply(lambda x: len(set(x["genres"].split("|")) & user_genres),
                                         axis=1)
    return d_f


def ask_genres():
    """
    () -> (set)
    Prints information about recommendation system.
    Asks user about his/her favourite genres of the films.
    """
    print('Enter number of your favourite genre. '
          'If you don`t want to enter more genres, enter "Stop".')

    lst_all_genres = ['Action', 'Adventure',
                      'Animation', 'Children`s',
                      'Comedy', 'Crime',
                      'Documentary', 'Drama',
                      'Fantasy', 'Film-Noir',
                      'Horror', 'Musical',
                      'Mystery', 'Romance',
                      'Sci-Fi', 'Thriller',
                      'War', 'Western']

    for i in range(1, len(lst_all_genres) + 1):  # prints all possible genres
        print('{}. {}'.format(i, lst_all_genres[i - 1]))
    print('')

    set_fav_genres = set()

    chosen_genres = 0
    while True:  # ask user about his favourite genres
        try:
            genre_num = input("You like genre: ")
            if genre_num == 'Stop' or genre_num == 'Stop'.lower():
                if chosen_genres < 3:
                    print('You have chosen only {} genres. '
                          'Please, choose at least 3 genres.'.format(chosen_genres))
                else:
                    break

            elif chosen_genres == 18:
                print('You have chosen all genres! You`re a big movie lover! '
                      'Now it`s time to rate some films.')
                break

            elif 1 <= int(genre_num) <= 18:
                if lst_all_genres[int(genre_num) - 1] not in set_fav_genres:
                    set_fav_genres.add(lst_all_genres[int(genre_num) - 1])
                    chosen_genres += 1
                else:
                    print('You have already chosen this genre!')

            else:
                print('Please, enter value in range from 1 to 18. Try again.')

        except ValueError:
            print('Please, enter integer value in range from 1 to 18. Try again.')

    return set_fav_genres


def ask_ratings(films):
    """
    (Series) -> (dict)
    Print best films of user`s favourite genres
    one by one and asks how user can evaluate
    the film from 0.5 to 5.

    Return dictionary, where keys are
    films names and values are user`s ratings.
    """
    ratings = dict()
    print('\nPlease, enter rating for 20 films or more.\nIf you don`t '
          'know the film - enter "Skip".\nIf you want to finish evaluating - '
          'enter "Stop".\nEnter the rating in range from 0.5 to 5 with half-point increment.')
    for _, val in films.iteritems():  # ask user about rating
        print('\nHow can you rate this film?')
        print(val)
        while True:
            try:
                rating = input('Your rating: ')
                if '0.5' <= rating <= '5.0' and (len(rating) == 1 or (len(rating) == 3 and
                                                                      (rating.endswith('0') or
                                                                       rating.endswith('5')))):
                    ratings[val] = float(rating)
                    break
                if (rating == 'Stop' or rating == 'Stop'.lower()) and len(ratings) < 20:
                    print('You have rated only {} films. Rate at least '
                          '20 films.\nFor more accurate recommendations, '
                          'please, rate as much films as you can.'.format(len(ratings)))
                elif rating == 'Stop' or rating == 'Stop'.lower() or \
                        rating == 'Skip' or rating == 'Skip'.lower():
                    break
                else:
                    print('Please, enter rating in range from 0.5 to 5 with half-point increment.\n'
                          'Also you can enter "Skip" to skip rating this film, or "Stop" to stop '
                          'rating films.')
                    continue
            except (ValueError, TypeError):
                print('Please, enter rating in range from 0.5 to 5 with half-point increment.\n'
                      'Also you can enter "Skip" to skip rating this film, or "Stop" to stop '
                      'rating films.')
        if rating == 'Stop' or rating == 'Stop'.lower():
            break

    return ratings


def main():
    """
    () -> (Dataframe)
    Main function
    """
    print('Here you can choose at least 3 of your favourite genres and '
          'rate at least 20 films of these genres. \nWe will generate '
          'list of films that you will like (we hope so).\n')

    fav_genres = ask_genres()

    data = pd.read_csv(final)  # create dataframe with films, ratings, number of votes

    data = data.loc[data['numVotes'] >= 100000]  # deleting films with less then 100 000 votes

    filtered_data = filter_films(fav_genres, data)  # create dataframe with films of genres, chosen by user

    filtered_data['averageRating'] = filtered_data.apply(lambda row: round(row.averageRating),
                                                         axis=1)  # round films` ratings

    filtered_data = filtered_data.sort_values(['averageRating', 'number_fav_genres', 'numVotes'],
                                              ascending=(False, False, False))  # sort films

    films_to_rate_df = filtered_data['title']  # create Series-object of films, that are sorted
    # from the most popular to the least popular

    user_ratings = ask_ratings(films_to_rate_df)  # ask user`s opinion about films

    user_ratings_df = pd.DataFrame(user_ratings.items(), columns=['title', 'rating'])

    user_ratings_df = pd.merge(user_ratings_df, filtered_data, on='title', how='inner')
    del user_ratings_df['averageRating']
    del user_ratings_df['numVotes']
    del user_ratings_df['genres']
    del user_ratings_df['number_fav_genres']

    user_id = [0 for _ in range(len(user_ratings_df['rating']))]
    user_ratings_df['userId'] = user_id

    return user_ratings_df
