""" Test game logic """

import py2048


def check_correct_num(board, indices, expected):
    not_equal = 0
    for index, num in zip(indices, expected):
        if board[index] != num:
            not_equal += 1
    assert not_equal == 1


def check_reset(game):
    assert game.score == 0
    assert len(game._empty) == len(game.board) - 2
    assert game.isover == False


def check_score(got, expected):
    assert got == expected


def check_empty_tile(game, filled):
    not_equal = 0
    for i in range(len(game.board)):
        if i in filled:
            assert i not in game._empty
        elif i not in game._empty:
            not_equal += 1
    assert not_equal == 1


def test_basic():
    game = py2048.Game()
    assert game._size == 4
    assert game._ntiles == 16
    _ = repr(game)
    check_reset(game)
    game._board = [
        2, 2, 4, 4,
        0, 2, 0, 4,
        2, 0, 0, 0,
        2, 0, 2, 4
    ]
    game._empty = {0, 1, 2, 3, 5, 7, 8, 12, 14, 15}
    game._score = 0
    game.moveleft()
    board = game._board
    check_correct_num(board, range(16),
                      [4, 8, 0, 0,
                       2, 4, 0, 0,
                       2, 0, 0, 0,
                       4, 4, 0, 0])
    check_empty_tile(game, {0, 1, 4, 5, 8, 12, 13})
    check_score(game.score, 16)

    game._board = [
        4, 8, 0, 0,
        2, 4, 0, 0,
        2, 0, 0, 0,
        4, 4, 0, 0
    ]
    game._empty = {0, 1, 4, 5, 8, 12, 13}
    game._score = 0
    game.moveup()
    board = game._board
    check_correct_num(board, range(16),
                      [4, 8, 0, 0,
                       4, 8, 0, 0,
                       4, 0, 0, 0,
                       0, 0, 0, 0])
    check_empty_tile(game, {0, 1, 4, 5, 8})
    check_score(game.score, 12)

    game._board = [
        4, 8, 0, 0,
        4, 8, 0, 0,
        4, 0, 0, 0,
        0, 0, 0, 0
    ]
    game._empty = {0, 1, 4, 5, 8}
    game._score = 0
    game.movedown()
    board = game._board
    check_correct_num(board, range(16),
                      [0, 0, 0, 0,
                       0, 0, 0, 0,
                       4, 0, 0, 0,
                       8, 16, 0, 0])
    check_empty_tile(game, {8, 12, 13})
    check_score(game.score, 24)

    game._board = [
        0, 0, 0, 0,
        0, 0, 0, 0,
        4, 0, 0, 0,
        8, 16, 0, 0
    ]
    game._empty = {8, 12, 13}
    game._score = 0
    game.moveright()
    board = game._board
    check_correct_num(board, range(16),
                      [0, 0, 0, 0,
                       0, 0, 0, 0,
                       0, 0, 0, 4,
                       0, 0, 8, 16])
    check_empty_tile(game, {11, 14, 15})
    check_score(game.score, 0)

    game.reset()
    check_reset(game)

    game._board = [
        512, 256, 128, 64,
        32, 16, 8, 4,
        4, 8, 16, 32,
        0, 128, 256, 512
    ]
    game._empty = {12}
    game.movedown()
    assert game.isover
    check_empty_tile(game, set(range(1, 16)))

    game = py2048.Game(5)
    assert game._size == 5
    assert game._ntiles == 25
    check_reset(game)
