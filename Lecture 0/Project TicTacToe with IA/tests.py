"""
Tic Tac Toe Player
"""
import copy
import math

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

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counts = sum(item == X for sublist in board for item in sublist)
    o_counts = sum(item == O for sublist in board for item in sublist)

    return X if x_counts == o_counts else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row_num in enumerate(board):
        for col_num in enumerate(row_num[1]):
            if col_num[1] == EMPTY:
                possible_actions.add((row_num[0], col_num[0]))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise ValueError(f"Invalid Action on position {action} for board {board}.")

    p_symbol = player(board)
    final_board = copy.deepcopy(board)
    final_board[action[0]][action[1]] = p_symbol

    return final_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check row win condition
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]

    # Check column win condition
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    # Check diagonal win condition
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len(actions(board)) == 0 or winner(board) is not None:
        return True
    else:
        False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player_winner = winner(board)
    return 1 if player_winner == X else -1 if player_winner == O else 0


def max_value(board, play, prune=float('inf')):
    if terminal(board):
        return utility(board), play

    v = float('-inf')
    for action in actions(board):
        score, _ = min_value(result(board, action), play=action, prune=v)
        if score > v:
            v = score
            best_play = action
        if score > prune:
            return v, best_play

    return v, best_play


def min_value(board, play, prune=float('-inf')):
    if terminal(board):
        return utility(board), play

    v = float('inf')
    for action in actions(board):
        score, _ = max_value(result(board, action), play=action, prune=v)
        if score < v:
            v = score
            best_play = action
        if score < prune:
            return v, best_play

    return v, best_play


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return max_value(board, play=None)[1]
    else:
        return min_value(board, play=None)[1]


test_board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, X],
            [X, EMPTY, X]]

print(minimax(initial_state()))