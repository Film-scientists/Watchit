"""
Module with tests
"""
import unittest
from ..auth import User, authenticator, AuthException
from ..data import users


class AuthTest(unittest.TestCase):
    """Module for testing auth.py"""
    def setUp(self):
        """
        Do the set-up
        """
        self.user_1 = User('test_user', '123456')
        self.authentificator = authenticator

    def test_exceptions(self):
        """
        Test for exceptions
        """
        self.assertIsInstance(AuthException('user'), AuthException, 'Not AuthException object.')

    def test_user(self):
        """
        User oriented test
        """
        self.assertTrue(self.user_1.check_password('123456'), 'Wrong password check.')
        self.assertFalse(self.user_1.check_password('123456s'), 'Right password check.')

    def test_authenticator(self):
        """
        Test for authentication
        """
        self.assertFalse(self.authentificator.add_user('DR', '123456'), 'Wrong user added.')
        self.assertTrue(self.authentificator.login('DR', '123456'), 'User login failed.')
        self.assertTrue(self.authentificator.is_logged_in("DR"), 'User is not logged in.')
        self.assertFalse(self.authentificator.is_logged_in("Evan"), 'Wrong user is logged in.')


def main():
    """
    Run tests for auth.py
    """
    test = AuthTest()
    test.setUp()
    test.test_exceptions()
    print("test_exceptions - passed")
    test.test_user()
    print("test_user - passed")
    test.test_authenticator()
    print("test_authenticator - passed")
    lines = None
    with open(users, mode="r", encoding="UTF-8") as file:
        lines = file.readlines()
    with open(users, mode="w", encoding="UTF-8") as file:
        for line in lines[:-1]:
            file.write(line)
