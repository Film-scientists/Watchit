"""
Module with Authenticator
"""

import hashlib
from pathlib import Path
from .data import users


class AuthException(Exception):
    """
    Represent main exception class
    """
    def __init__(self, username, user=None):
        """
        :param username: value
        :param user: value
        ------------------
        Initialize object
        """
        super().__init__(username, user)
        self.username = username
        self.user = user


class UsernameAlreadyExists(AuthException):
    """
    Represent AuthException subclass
    """


class PasswordTooShort(AuthException):
    """
    Represent AuthException subclass
    """


class InvalidUsername(AuthException):
    """
    Represent AuthException subclass
    """


class InvalidPassword(AuthException):
    """
    Represent AuthException subclass
    """


class NotLoggedInError(AuthException):
    """
    Represent AuthException subclass
    """


class User:
    """
    Class for user representation.
    """

    def __init__(self, username, password):
        """
        (User, str, str) -> NoneType
        Create a new user object. The password
        will be encrypted before storing.
        """
        self.username = username
        self.password = self._encrypt_pw(password)
        self.is_logged_in = False

    def _encrypt_pw(self, password):
        """
        (User, str) -> str
        Encrypt the password with the username and return
        the sha digest.
        """
        hash_string = self.username + password
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()

    def check_password(self, password):
        """
        (User, str) -> bool
        Return True if the password is valid for this
        user, false otherwise.
        """
        encrypted = self._encrypt_pw(password)
        return encrypted == self.password

    def __str__(self):
        """
        :return: str
        ------------
        Return string representation of the object
        """
        return str(self.username)


class Authenticator:
    """
    Class for authenticator representation.
    """

    def __init__(self):
        """
        (Authenticator) -> NoneType
        Construct an authenticator to manage
        users logging in and out.
        """
        self.users = {}
        self.data_file = users
        with open(self.data_file, 'r', encoding='UTF-8') as user_f:
            data_txt = user_f.readlines()
            if len(data_txt) != 0:
                for line in data_txt:
                    line = line.split()
                    self.users[line[0]] = User(line[0], line[1])
        user_f.close()
        try:
            sys_files = Path('sys_data/')
            sys_files.mkdir()
        except FileExistsError:
            pass

    def add_user(self, username, password):
        """
        (Authenticator) -> NoneType
        Adds a new user.
        """
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if len(password) < 6:
            raise PasswordTooShort(username)
        self.users[username] = User(username, password)
        with open(self.data_file, 'a', encoding='UTF-8') as user_f:
            user_f.write(username + ' ' + password + '\n')
        user_f.close()

    def login(self, username, password):
        """
        (Authenticator, str, str) -> bool
        Logins user.
        """
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)

        if not user.check_password(password):
            raise InvalidPassword(username, user)

        user.is_logged_in = True
        return True

    def is_logged_in(self, username):
        """
        (Authenticatior, str) -> bool
        Checks whether user is logged.
        """
        if username in self.users:
            return self.users[username].is_logged_in
        return False


authenticator = Authenticator()
