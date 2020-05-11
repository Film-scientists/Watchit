"""
module with FilmSystem class
"""
from . import auth
from . import recomendation_engine


class FilmSystem:
    """
    Class for film system representation.
    """
    def __init__(self):
        """
        (FilmSystem) -> NoneType
        Create a new object of FilmSystem class.
        """
        self.username = None
        self.menu_map = {
            "register": self.register,
            "login": self.login,
            "see": self.see,
            "get": self.get,
            "quit": self.quit,
        }

    def login(self):
        """
        (FilmSystem) -> NoneType
        Logins user.
        """
        username = input("username: ").strip()
        password = input("password: ").strip()
        try:
            auth.authenticator.login(username, password)
        except auth.InvalidUsername:
            print("Sorry, that username does not exist")
            return True
        except auth.InvalidPassword:
            print("Sorry, incorrect password")
            return True
        else:
            print('You successfully logged in.')
            self.username = username
            self.create_txt()
            return False

    def register(self):
        """
        (FilmSystem) -> NoneType
        Registers user.
        """
        new_username = input("Enter username: ").strip()
        new_psw = input("Enter password: ").strip()
        try:
            auth.authenticator.add_user(new_username, new_psw)
            auth.authenticator.login(new_username, new_psw)

        except auth.InvalidUsername:
            print("\nSorry, that username does not exist")
            return True
        except auth.InvalidPassword:
            print("\nSorry, incorrect password")
            return True
        except auth.PasswordTooShort:
            print('\nPassword too short.')
            return True
        except auth.UsernameAlreadyExists:
            print('\nUsername already exists.')
            return True
        else:
            print('\nYou successfully registered.')
            self.username = new_username
            self.create_txt()
            return False

    def create_txt(self):
        """
        (FilmSystem) -> NoneType
        Creates file for storing user data.
        """
        try:
            _ = open(f'sys_data/{self.username}.txt', 'r')
        except FileNotFoundError:
            _ = open(f'sys_data/{self.username}.txt', 'w')

    def see(self):
        """
        (FilmSystem) -> NoneType
        Viewing function.
        """
        with open(f'sys_data/{self.username}.txt', 'r') as user_films:
            films = user_films.readlines()
            if len(films) == 0:
                print('Oups, looks like you do not have recommended films yet.')
            else:
                for film in films:
                    print(film, end='')

    def get(self):
        """
        (FilmSystem) -> NoneType
        Recommends films to usser based on collaborative filtering algorythm.
        """
        user_films = recomendation_engine.core()
        with open(f'sys_data/{self.username}.txt', 'w', encoding="UTF-8") as user_f:
            for film in user_films:
                user_f.write(film+'\n')
        user_f.close()

    @staticmethod
    def quit():
        """
        (FilmSystem) -> NoneType
        Quits the module.
        """
        raise SystemExit()

    def menu(self):
        """
        (FilmSystem) -> str
        Main menu function.
        """
        try:
            first_step = True
            print('Welcome to the best recommendation system ever!'.center(120))
            while first_step:
                print(
                    """
Please log in if you already have an account:
            Enter 'login'
Or register if you are new to our app:
           Enter 'register'
Want ot quit?
            Enter 'quit'
""")
                answer = input("What you want to do: ").lower()
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print(f"{answer} is not a valid option")
                else:
                    first_step = func()
            while True:
                print("""
What would you like to do next:
> Get personal recommendations - enter 'get'
> See prevoius recommendations - enter 'see' 

> Quit - enter 'quit'
""")
                answer = input().lower()
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print(f"{answer} is not a valid option")
                else:
                    func()
        except SystemExit:
            print('Exitting..')


if __name__ == "__main__":
    FilmSystem().menu()
