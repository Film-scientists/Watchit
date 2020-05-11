"""
Matrix algorithm
"""
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

RANK = 50


def make_matrix(sbr):
    """
    Algorithm
    Return predictions
    """
    r_df = sbr.matrix()
    r_m = r_df.values
    user_ratings_mean = np.mean(r_m, axis=1)
    r_demeaned = r_m - user_ratings_mean.reshape(-1, 1)
    # Algorithm
    u_m, sigma, vt_m = svds(r_demeaned, k=RANK)
    sigma = np.diag(sigma)
    all_user_predicted_ratings = np.dot(np.dot(u_m, sigma), vt_m).astype("float32") + \
                                 user_ratings_mean.reshape(-1, 1).astype("float32")
    # Algorithm
    predictions = pd.DataFrame(all_user_predicted_ratings, columns=r_df.columns)
    return predictions


def recommend_movies(predictions_df, user_id, movies_df, sbr, num_recommendations=5):
    """
    Sorts predictions
    Return top <num_recommendations> for user <userID>
    """
    # Get and sort the user's predictions
    sorted_user_predictions = predictions_df[user_id] \
        .sort_values(ascending=False) \
        .reset_index()  # UserID starts at 1
    # Get the user's data and merge in the movie information.
    user_frame = sbr.main_user.data_frame
    recommendations = (movies_df[~movies_df['movieId'].isin(user_frame['movieId'])].
                       merge(pd.DataFrame(sorted_user_predictions), how='right',
                             left_on='movieId',
                             right_on='index').
                       rename(columns={user_id: 'Predictions'}).
                       sort_values('Predictions', ascending=False).
                       iloc[:num_recommendations * 10, :-1])
    recommendations.drop(["index"], axis=1, inplace=True)
    recommendations.dropna(inplace=True)
    return recommendations.head(num_recommendations).reset_index(drop=True)[:num_recommendations]


def matrix_fct(saber, movies, pred_num):
    """
    Main module
    """
    predictions = make_matrix(saber)
    rec = recommend_movies(predictions, -1, movies, saber, pred_num)
    return rec
