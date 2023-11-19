import numpy as np
import pandas as pd

# Load Data Set for AI
data = pd.read_csv("tic-tac-toe.csv")
print(data.info())
print()
print(data.head())


def search(board):
    """
    search() performs a search of a given board for the best possible move

    :param board:
    :return: (row, col) for best move
    """
    # Will handle search for best_move()
    # MAY BE MERGED WITH best_move()
    # should use data to determine best move
    # TODO: Implement search method (Alpha-Beta preferable)
    return (0, 0)


def best_move(letter, board):
    # Should perform search to find best move
    # will then run best move
    move = search(board)


    return
