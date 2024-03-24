"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board) -> str:
    """
    Returns player who has the next turn on a board. Assumes X goes first, so if there are an even number of Xs on the
    board, returns O, otherwise returns X.
    """
    return X if sum([board[i].count(X) for i in range(3)]) % 2 == 0 else O


def actions(board: list[list]) -> set[tuple]:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for r, row in enumerate(board):
        for c, column in enumerate(row):
            if column != EMPTY:
                moves.add((r, c))

    return moves


def result(board: list[list], action: tuple[int]) -> list[list]:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row = action[0]
    column = action[1]
    if board[row][column] != EMPTY:
        raise Exception(f"Invalid move - position {row}, {column} already occupied with {board[row][column]}")

    new_board = copy.deepcopy(board)
    new_board[row][column] = player(new_board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
