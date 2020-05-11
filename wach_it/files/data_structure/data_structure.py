"""
Module with DataStructure
"""
from math import sqrt
import ctypes
from collections import UserList
import pandas as pd
import numpy as np


class Array:
    """
    Represent array
    """
    def __init__(self, size):
        """
        :param size: int ( > 0)
        -----------------------
        Initialize array object
        """
        assert size > 0, "Array size must be > 0"
        self._size = size
        py_array_type = ctypes.py_object * size
        self._elements = py_array_type()
        self.clear(None)

    def __len__(self):
        """
        :return: int
        ------------
        Return length of array
        """
        return self._size

    def __getitem__(self, index):
        """
        :param index: int (0 < index < len(array))
        :return: any
        ------------
        Return the item stored in cell with given index
        """
        assert 0 <= index < len(self), "Array subscript out of range"
        return self._elements[index]

    def __setitem__(self, index, value):
        """
        :param index: int (0 < index < len(array))
        :param value: any
        :return: None
        -------------
        Set given value into given cell with given position
        """
        assert 0 <= index < len(self), "Array subscript out of range"
        self._elements[index] = value

    def clear(self, value):
        """
        :param value: any
        :return: None
        -------------
        Change items in all the cells to value
        """
        for i in range(len(self)):
            self._elements[i] = value

    def __iter__(self):
        """
        :return: object of _ArrayIterator class
        ---------------------------------------
        Enable iteration with for loop, etc
        """
        return _ArrayIterator(self._elements)


class _ArrayIterator:
    """
    Represent iterator
    """
    def __init__(self, the_array):
        """
        :param theArray: array object
        -----------------------------
        Initialize iterator object
        """
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        """
        :return: instance of _ArrayIterator class
        """
        return self

    def __next__(self):
        """
        :return: any or raise StopIteration
        -----------------------------------
        Return next element of array if possible
        Otherwise, raise StopIteration
        """
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        raise StopIteration


class User:
    """
    Represent user object
    """
    def __init__(self, user_id, ratings):
        """
        :param user_id: int
        :param ratings: DataFrame
        -------------------------
        Initialize the user object
        """
        self.u_id = user_id
        self.data_frame = ratings
        self.av_r = self.get_average_rating(ratings)
        self.norm_r = self.normalize_ratings(ratings)
        self.weight = None

    @staticmethod
    def get_average_rating(ratings):
        """
        :param ratings: DataFrame
        :return: number
        ---------------
        Return the average rating that user gives to film
        """
        return round(ratings["rating"].mean())

    def normalize_ratings(self, ratings):
        """
        :param ratings: DataFrame
        :return: dict
        -------------
        Return dict with normalized ratings
        the keys() are movieId
        the items() are ratings themselves
        """
        norm_rates = {}
        dct = ratings.to_dict()
        movie_id, rating = dct["movieId"], dct["rating"]
        for ind, movie in movie_id.items():
            norm_rates[movie] = rating[ind] - self.av_r
        return norm_rates

    def get_movies(self):
        """
        :return: set
        ------------
        Return all the movies that particular user has rated
        """
        return set(self.norm_r.keys())

    def weighting(self, other):
        """
        :param other: User
        :return: number or None
        -----------------------
        IF user[other] is significant
        Return number - Its weight
        Otherwise - Return False
        """
        both = set(self.norm_r.keys()) & set(other.norm_r.keys())
        if len(both) >= 10:
            tg_u = Array(len(both))
            u_2 = Array(len(both))
            i = 0
            for film in both:
                tg_u[i] = self.norm_r[film]
                u_2[i] = other.norm_r[film]
                i += 1
            numerator = 0
            denominator_1 = 0
            denominator_2 = 0
            for i, elm in enumerate(tg_u):
                numerator += elm * u_2[i]
                denominator_1 += elm ** 2
                denominator_2 += u_2[i] ** 2
            if numerator == 0:
                return None
            weight = numerator / (sqrt(denominator_1) * sqrt(denominator_2))
            return round(weight, 2)
        return None

    def set_weight(self, weight):
        """
        :param weight: number
        :return: None
        -------------
        Set weight parameter
        """
        self.weight = weight

    def __str__(self):
        """
        :return: str
        ------------
        Return string representation
        """
        return f"<->\n" \
               f"User: {self.u_id}\n" \
               f"average_rate: {str(self.av_r)}\n" \
               f"<->\n"

    def __repr__(self):
        """
        :return: str
        ------------
        Represent object
        """
        return str(self.u_id) + '-' + str(self.weight)


class Saber:
    """
    Represent slicer
    """
    def __init__(self, file_name):
        """
        :param file_name: str
        ---------------------
        Initialize
        """
        self.lst = UserList()
        self.main_user = None
        self.important = []
        lst = self.lst
        user_dict = {}
        for elm in pd.read_csv(file_name, chunksize=100000):
            elm.drop("timestamp", inplace=True, axis=1)
            elm = elm.groupby(["userId"])
            for u_i, grp in elm:
                grp = grp.drop("userId", axis=1)
                if u_i in user_dict:
                    index = user_dict[u_i]
                    lst[index] = pd.concat([lst[index], grp], ignore_index=True)
                else:
                    user_dict[u_i] = len(lst)
                    lst.append(grp)
        for ind, elm in enumerate(lst):
            lst[ind] = User(ind+1, elm.reset_index(drop=True))

    def __iter__(self):
        """
        :return: _ArrayIterator
        -----------------------
        Make object iterable
        """
        return _ArrayIterator(self.lst)

    def all_movies(self):
        """
        :return: set
        ------------
        Return all the movies that users have seen
        """
        movies = set()
        for elm in self:
            movies.update(elm.get_movies())
        return movies

    def __len__(self):
        """
        :return: int
        ------------
        Return the number of users excluding the main_user
        """
        return len(self.lst)

    def matrix(self):
        """
        :return: DataFrame
        ------------------
        Make a matrix to be used in the algorithm
        """
        assert self.main_user is not None and len(self) != 0
        films = sorted(self.all_movies())
        users = list(range(-1, len(self)))
        size_f, size_u = len(films), len(self) + 1
        zero = np.zeros([size_f, size_u])
        frame = pd.DataFrame(zero, index=films, columns=users)
        frame[-1] = self.main_user.data_frame.set_index("movieId")
        for ind in users[1:]:
            frame[ind] = self[ind].data_frame.set_index("movieId")
        return frame.fillna(0)

    def __getitem__(self, index):
        """
        :param index: int
        :return: User
        -------------
        Return User instance
        """
        assert -1 < index < len(self) and isinstance(index, int)
        return self.lst[index]

    def is_important(self, user):
        """
        :param user: User
        :return: None
        -------------
        Append user that will be used in the nearest neighbour algorithm
        """
        self.important.append(user)

    def set_main(self, data):
        """
        :param data: DataFrame
        :return: None
        -------------
        Initialize main_user
        # data should have at least "rating" and "movieId" columns
        """
        data = data[["rating", "movieId"]]
        self.main_user = User("MAIN", data.reset_index(drop=True))
