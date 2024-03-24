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
    Returns player who has the next turn on a board. Assumes X goes first, so if there's an odd number of empty spaces
    it's X's turn, otherwise it's O's turn.
    """
    return O if sum([board[i].count(EMPTY) for i in range(3)]) % 2 == 0 else X


def actions(board: list[list]) -> set[tuple[int, int]]:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for r, row in enumerate(board):
        for c, column in enumerate(row):
            if column == EMPTY:
                moves.add((r, c))

    return moves


def result(board: list[list], action: tuple[int, int]) -> list[list]:
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


def winner(board: list[list]) -> None | str:
    """
    Returns the winner of the game, if there is one.
    """
    x_winner = {X}
    o_winner = {O}

    # Check for horizontal winners
    if any(set(row) == x_winner for row in board):
        return X
    if any(set(row) == o_winner for row in board):
        return O

    # Check for vertical winners
    first_column = (board[0][0], board[1][0], board[2][0])
    second_column = (board[0][1], board[1][1], board[2][1])
    third_column = (board[0][2], board[1][2], board[2][2])
    columns = (first_column, second_column, third_column)
    if any(set(column) == x_winner for column in columns):
        return X
    if any(set(column) == o_winner for column in columns):
        return O

    # Check for diagonal winners
    main_diagonal = (board[0][0], board[1][1], board[2][2])
    anti_diagonal = (board[0][2], board[1][1], board[2][0])
    if set(main_diagonal) == x_winner:
        return X
    if set(main_diagonal) == o_winner:
        return O
    if set(anti_diagonal) == x_winner:
        return X
    if set(anti_diagonal) == o_winner:
        return O

    return None


def terminal(board: list[list]) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    all_board_moves = [board[i][j] for i in range(len(board)) for j in range(len(board[0]))]
    if EMPTY not in all_board_moves:
        return True

    return False


def utility(board: list[list]) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    if winning_player == O:
        return -1

    return 0


def minimax(board: list[list]) -> None | tuple[int, int]:
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    moves = actions(board)
    if player(board) == X:
        return max([(action, min_value(result(board, action))) for action in moves], key=lambda x: x[1])[0]

    return min([(action, max_value(result(board, action))) for action in moves], key=lambda x: x[1])[0]


def max_value(board: list[list]) -> int:
    if terminal(board):
        return utility(board)

    value = float("-inf")
    for action in actions(board):
        value = max(value, min_value(result(board, action)))

    return value


def min_value(board: list[list]) -> int:
    if terminal(board):
        return utility(board)

    value = float("inf")
    for action in actions(board):
        value = min(value, max_value(result(board, action)))

    return value
