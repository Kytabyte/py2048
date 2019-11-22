from .game import Game
from .ui import terminal_run

__all__ = ['Game']
__version__ = '0.1.0'
__author__ = 'Kyle Xie'


def start(size):
    terminal_run(size)
