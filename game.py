import random as rnd
from enum import Enum

ELEMENTS_TYPES = [[[1]],
                  [[1, 1], [1, 1]],
                  [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                  [[1, 1, 1]],
                  [[1, 1], [1, 0]],
                  [[1], [1]],
                  [[0, 1, 0], [1, 1, 1]],
                  [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
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
        self._field = []
        self._rc = row_count
        self._cc = col_count
        self._state = GameState.UNK
        self._kit = []
        self._curr = None
        self._f = True
        self.new_game()

    def new_game(self):
        self._field = [[0 for _ in range(self.col_count)] for _ in range(self.row_count)]
        self._kit = [Element(ELEMENTS_TYPES[rnd.randint(0, len(ELEMENTS_TYPES)) - 1]) for _ in range(3)]
        self._state = GameState.PLAYING

    def _game_over(self):
        for el in self.kit:
            r = len(el.it)
            c = len(el.it[0])
            dr = self._rc - r
            dc = self._cc - c
            for n in range(dr + 1):
                for m in range(dc + 1):
                    if self._can_placed(el.it, n, m): return False
        return True

    def _can_placed(self, elem, r, c):
        rc = len(self._field)
        cc = len(self._field[0])
        if r + len(elem) > rc or c + len(elem[0]) > cc:
            return False
        for i, j in all_combs(len(elem), len(elem[0])):
            if elem[i][j] == 1 and self.field[r + i][c + j] == 1:
                return False
        return True

    def _place(self, elem, r, c, flag):
        re = len(elem)
        ce = len(elem[0])
        for i in range(r, r + re):
            for j in range(c, c + ce):
                if not flag:
                    mult = 1 if self._field[i][j] == 1 else -1
                    self._field[i][j] = mult * (self._field[i][j] + elem[i - r][j - c])
                else:
                    self._field[i][j] = self.field[i][j] ** 2

    def _check_rows(self):
        res = []
        for i in range(len(self._field)):
            j = 0
            while j < len(self._field) and self._field[i][j] == 1:
                j += 1
            if j == len(self._field): res.append(i)
        return res

    def _check_columns(self):
        res = []
        for j in range(len(self._field)):
            i = 0
            while i < len(self._field) and self._field[i][j] == 1:
                i += 1
            if i == len(self._field): res.append(j)
        return res

    def _clear_row(self, r):
        for j in range(len(self._field)):
            self._field[r][j] = 0

    def _clear_column(self, c):
        for i in range(len(self._field)):
            self._field[i][c] = 0

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
        if self._game_over(): self._state = GameState.LOSE
        return

    def elem_left_mouse_click(self, i):
        if self._state == GameState.PLAYING:
            self._curr = i

    def field_left_mouse_click(self, r, c, flag):
        if self._state == GameState.PLAYING:
            if self._curr is not None:
                if self._can_placed(self._kit[self._curr].it, r, c):
                    self._place(self._kit[self._curr].it, r, c, flag)
                    if flag:
                        self._kit[self._curr] = Element(ELEMENTS_TYPES[rnd.randint(0, len(ELEMENTS_TYPES)) - 1])

                        for i in self._check_rows():
                            self._clear_row(i)
                        for i in self._check_columns():
                            self._clear_column(i)

                    self._update()
                    return True
        return False

    def clear_opp(self):
        for i, j in all_combs(self.row_count, self.col_count):
            if self.field[i][j] < 0:
                self._field[i][j] = 0
