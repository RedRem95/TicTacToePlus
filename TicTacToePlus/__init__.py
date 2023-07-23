import os

from .game import Game

with open(os.path.join(os.path.dirname(__file__), "version.txt"), "r") as f_in:
    __version__ = f_in.readlines()[0].strip()

print(f"Using TicTacToePlus-v{__version__}")

del os
del f_in
