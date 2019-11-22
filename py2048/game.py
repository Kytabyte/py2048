""" The functionality of game py2048 """

import random

RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
PROB_TWO_TILE = 0.9


class Game:
    __slots__ = ['_size', '_ntiles', '_board', '_empty', '_score', '_isover', '_iter']

    def __init__(self, size: int = 4):
        if size < 2:
            raise ValueError("Input `size` must be greater than or equal to 2.")
        self._size = size
        self._ntiles = size * size
        self._iter = self._geniter()
        self.reset()

    def __repr__(self):
        size = self._size

        space = 8
        sep = '-' * space

        s = "GAME OVER!\n" if self.isover else ""
        s += f"Score: {self.score}\n"
        s += f" {sep * size}\n"
        s += f"\n {sep * size}\n".join(
                f"| {' | '.join(f'{self._board[i * size + j]:{space-3}d}' for j in range(size))}" + " |"
                for i in range(size))
        s += f"\n {sep * size}\n\n"

        return s

    def reset(self):
        self._score = 0
        self._board = [0] * self._ntiles
        self._empty = set(range(self._ntiles))
        self._isover = False
        self._fill(2)

    @property
    def board(self):
        return self._board

    @property
    def score(self):
        return self._score

    @property
    def isover(self):
        return self._isover

    def moveleft(self):
        return self._move(LEFT)

    def moveright(self):
        return self._move(RIGHT)

    def moveup(self):
        return self._move(UP)

    def movedown(self):
        return self._move(DOWN)

    def _move(self, direction):
        if self.isover:
            raise Exception("Game is Over. Call `reset` to start a new game.")

        move_any = False
        for strip in self._iter[direction]:
            move_any = self._move_zeros(strip) or move_any
            move_any = self._combine(strip) or move_any
        if move_any:
            self._update_empty()
            self._fill()

        return move_any

    def _geniter(self):
        # Since the combine strategy is the same for all directions of move,
        # we can generate the correct index traversal order for each direction then
        # write a single move function for all moves.
        #
        # hack of board traversal iterator using stride.
        #
        # Example of size of 4
        # Stride: (The index incremental along each dimension)
        # left (1, 4), up (4, 1), right (-1, 4), down (4, -1)
        #
        # E.g.
        # left traversal order (0, 1, 2, 3), (4, 5, 6, 7), ...
        # up traversal order (0, 4, 8, 12), (1, 5, 9, 13), ...
        # right and down traversal is the opposite of left and up respectively.
        size = self._size
        stride = (1, size)
        _iter = {
            LEFT: [[i * stride[1] + j * stride[0] for j in range(size)] for i in range(size)],
            UP:   [[i * stride[0] + j * stride[1] for j in range(size)] for i in range(size)]
        }
        _iter[RIGHT] = [strip[::-1] for strip in _iter[LEFT]]
        _iter[DOWN] = [strip[::-1] for strip in _iter[UP]]

        return _iter

    def _move_zeros(self, strip):
        move_any = False
        board = self._board

        zero = cur = 0
        while cur < len(strip):
            if board[strip[zero]] == 0 and board[strip[cur]] != 0:
                move_any = True
                board[strip[zero]], board[strip[cur]] = board[strip[cur]], board[strip[zero]]
            if board[strip[zero]] != 0:
                zero += 1
            cur += 1

        return move_any

    def _combine(self, strip):
        move_any = False

        board = self._board

        cur, zero = 0, 0
        while cur < len(strip):
            if board[strip[cur]] == 0:
                cur += 1
                continue
            if cur + 1 < len(strip) and board[strip[cur]] == board[strip[cur + 1]]:
                move_any = True
                board[strip[cur]] <<= 1
                self._score += board[strip[cur]]
                board[strip[cur + 1]] = 0
            if zero != cur:
                board[strip[zero]] = board[strip[cur]]
                board[strip[cur]] = 0
            if board[strip[zero]] != 0:
                zero += 1
            cur += 1

        return move_any

    def _update_empty(self):
        for i in range(self._ntiles):
            if self._board[i] == 0:
                self._empty.add(i)
            elif i in self._empty:
                self._empty.remove(i)

    def _fill(self, repeat=1):
        indices = random.sample(self._empty, repeat)
        for index in indices:
            tile = 2 if random.random() < PROB_TWO_TILE else 4
            self._board[index] = tile
            self._empty.remove(index)
            self._checkover(index)

    def _checkover(self, last_add):
        if self._empty:
            return

        board, size = self._board, self._size
        if (last_add % size != 0 and board[last_add] == board[last_add - 1] or
                last_add % size != size - 1 and board[last_add] == board[last_add + 1] or
                last_add // size != 0 and board[last_add] == board[last_add - size] or
                last_add // size != size - 1 and board[last_add] == board[last_add + size]):
            return

        self._isover = True

    def _addscore(self, score):
        self._score += score
