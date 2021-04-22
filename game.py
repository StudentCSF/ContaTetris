import random as rnd
from enum import Enum

ELEMENTS_TYPES = [[[1]],
                  [[1, 1], [1, 1]],
                  [[1, 1], [1, 1], [1, 1]],
                  [[1, 1, 1]],
                  [[1, 1], [1, 0]],
                  [[1], [1]],
                  [[0, 1, 0], [1, 1, 1]],
                  [[1, 1, 1], [0, 0, 1], [0, 1, 1]],
                  [[1, 1], [0, 1], [0, 1]],
                  [[1], [1, 1, 1]],
                  [[1, 1, 1, 1]],
                  [[1], [1], [1], [1]]
                  ]


def all_combs(n, m):
    for i in range(n):
        for j in range(m):
            yield i, j


class GameState(Enum):
    UNK = -1
    PLAYING = 0
    LOSE = 1


class Element:
    def __init__(self, it):
        self._it = it

    @property
    def it(self):
        return self._it


class Game:
    def __init__(self, row_count, col_count):
        self._field = [[0 for _ in range(col_count)] for _ in range(row_count)]
        self._rc = row_count
        self._cc = col_count
        self._state = GameState.UNK
        self._kit = [Element(ELEMENTS_TYPES[rnd.randint(0, len(ELEMENTS_TYPES)) - 1]) for _ in range(3)]
        self.new_game()

    def new_game(self):
        self._state = GameState.PLAYING

    def _game_over(self):
        for el in self.kit:
            r = len(el)
            c = len(el[0])
            dr = self._rc - r
            dc = self._cc - c
            for n in range(dr + 1):
                for m in range(dc + 1):
                    if self.can_placed(el, n, m): return False
        return True

    def _can_placed(self, elem, r, c):
        for i, j in all_combs((len(elem), len(elem[0]))):
            if elem[i][j] == 1 and self.field[r + i][c + j] == 1:
                return False
        return True

    def _place(self, elem, r, c):
        re = len(elem)
        ce = len(elem[0])
        for i in range(r, r + re):
            for j in range(c, ce):
                self._field[i][j] = self.field[i][j] + elem[i - r][j - ce]

    def check_lines(self):
        res = []
        for i in range(len(self._field)):
            j = 0
            while j < len(self._field) and self._field[i][j] == 1:
                j += 1
            if j == len(self._field): res.__add__(i)

    @property
    def field(self):
        return self._field

    @property
    def row_count(self):
        return self._rc

    @property
    def col_count(self):
        return self._cc

    @property
    def state(self):
        return self._state

    @property
    def kit(self):
        return self._kit

    def _update(self):
        return
