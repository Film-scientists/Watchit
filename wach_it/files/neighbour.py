"""
Module with neighbour algorithm
"""
import pandas as pd


def nearest_n(movies, saber, pred_num):
    """
    :return: DataFrame
    ------------------
    Execute the algorithm
    print top n predictions
    Return all the predictions
    """
    target_user = saber.main_user
    for user in saber:
        weight = target_user.weighting(user)
        user.set_weight(weight)
        if weight is not None and weight >= 0.5:
            saber.is_important(user)

    important = saber.important
    important.sort(key=lambda x: x.weight, reverse=True)

    neighbors = important[:30]
    sum_w = 0
    for user in neighbors:
        sum_w += user.weight

    watched = target_user.norm_r.keys()
    predictions = []

    for movie in movies['movieId']:
        if movie in watched:
            continue
        p_movie = 0
        for user in neighbors:
            try:
                prp = user.norm_r[movie] * user.weight
                p_movie += prp
            except KeyError:
                continue
        try:
            predicted_r = target_user.av_r + (p_movie / sum_w)
            if predicted_r > 5:
                predicted_r = 5
            predictions.append((movie, round(predicted_r, 1)))
        except ZeroDivisionError:
            continue

    predictions.sort(key=lambda tup: tup[1], reverse=True)
    return pd.DataFrame(predictions, columns=["movieId", "rating"]).\
              merge(movies, how="left", left_on="movieId", right_on="movieId").\
              drop("rating", axis=1)[:pred_num]
