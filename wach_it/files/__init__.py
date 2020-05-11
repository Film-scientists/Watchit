"""
Some config
"""
import pathlib
from .data_structure import Saber

CONFIG = str(pathlib.Path(__file__).parent.absolute())

users = CONFIG + "/users.txt"
