"""
Main Processing module
"""
import concurrent.futures as ftr
import pandas as pd
from . import Saber
from .start import main
from .neighbour import nearest_n
from .matrix import matrix_fct
from .data import ratings, movies as films
from .data.test_only import test


TEST_FILE = test
MAIN_FILE = ratings
MOVIE_FILE = films
REC_NUM = 100  # Number of films to predict for each algorithm
REAL_REC = 20   # Number of recommended films to show to the users
COEFFICIENT = 0.7   # Roughly a proportion between films take from neighbour and matrix algorithm


def load(testing=False):
    """
    :return: DataFrame, Saber, DataFrame
    ------------------------------------
    Load all the necessary data
    """
    with ftr.ThreadPoolExecutor() as executor:
        saber = executor.submit(Saber, MAIN_FILE)
        movies = executor.submit(pd.read_csv, MOVIE_FILE)
        pivot = pd.read_csv(TEST_FILE) if testing else main()
        movies, saber = movies.result(), saber.result()
        saber.set_main(pivot)
    return movies, saber, pivot


def quintessential(pivot, rec_n, rec_m):
    """
    :param pivot: DataFrame
    :param rec_n: DataFrame
    :param rec_m: DataFrame
    :return: DataFrame
    ------------------
    Try to make the best prediction possible
    First filters genres and then ands intersection
    of results of two algorithms to their parts in certain
    proportion.
    Proportion depends on COEFFICIENT
    """
    genres = set()
    tem = REAL_REC
    d_f = None
    list(map(lambda ind: genres.update(set(pivot.iloc[ind]["genres"].split("|"))), pivot.index))
    intersection = rec_n.merge(rec_m, how="inner", on=["movieId", "title", "genres"])
    rec_n["check"], rec_m["check"] = map(
        lambda arg: arg.apply(
            lambda x: bool(set(x["genres"].split("|")) & genres) or None, axis=1), (rec_n, rec_m))
    list(map(lambda x: x.dropna(inplace=True), (rec_n, rec_m)))
    list(map(lambda x: x.drop("check", axis=1, inplace=True), (rec_n, rec_m)))
    inr_len = len(intersection)
    if inr_len:
        rec_n = rec_n[~rec_n['movieId'].isin(intersection['movieId'])]
        rec_m = rec_m[~rec_m['movieId'].isin(intersection['movieId'])]
        tem -= inr_len
        d_f = intersection
    d_f = pd.concat([d_f, rec_n[: round(tem * COEFFICIENT)]]) if d_f is not None \
        else rec_n[: round(tem * COEFFICIENT)]
    tem = REAL_REC - len(d_f)
    d_f = pd.concat([d_f, rec_m[: tem]]).reset_index(drop=True)
    return d_f


def core(testing=False):
    """
    :param testing: bool
    :return: DataFrame
    ------------------
    Run algorithms, prints
    and returns the best predictions
    """
    movies, saber, pivot = load(testing)
    if testing:
        pivot = pivot.merge(movies, how="left", on=["movieId"]).drop("genres", axis=True)
    pivot = pivot.merge(movies, how="left", on=["movieId", "title"])
    n_rec = nearest_n(movies, saber, REC_NUM)
    m_rec = matrix_fct(saber, movies, REC_NUM)
    final = quintessential(pivot, n_rec, m_rec) if not n_rec.empty else m_rec[:REAL_REC]
    line = "-------<User Recommendations>-------"
    print(line)
    user_lst = []
    for ind, elm in enumerate(final.iterrows()):
        print(f"{ind + 1}. {elm[1]['title']}")
        user_lst.append(f"{ind + 1}. {elm[1]['title']}")
    print(line)
    return user_lst
