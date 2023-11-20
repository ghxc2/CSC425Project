import numpy as np
import pandas as pd

# Load Data Set for AI
data = pd.read_csv("tic-tac-toe.csv")
print(data.info())
print()
print(data.head())

# LETTER FOR AI
ai_letter = "O"


def filter_chosen(board):
    """
    filter_chosen() will filter out all possible board combonations that have moves
    in line with that of the current game board
    :param board: board of the game being played
    :return: filtered dataset containing only possible future plays
    """
    # Create possible moves data to check with
    possible_moves = data.copy(True)

    # Loop through current game board
    for row in range(3):
        for col in range(3):
            # Determine what row of the table is being checked based on the database headers
            data_col = data.columns[(3 * row) + col]

            # Read current letter in spot on board
            spot = board[row][col]

            # Check if spot has been claimed
            if spot != "":

                if ai_letter == "O":
                    if spot == "X":
                        spot = "O"
                    if spot == "O":
                        spot = "X"

                # filter out impossible moves
                possible_moves = possible_moves.loc[data[data_col] == spot.lower()]

    return possible_moves


def filter_wins(possible_moves):
    """
    filter_wins() takes an input of possible games moves, and filters out all win conditions possible
    for future moves
    :param possible_moves: possible future moves, best from filter_chosen()
    :return: possible future wins the game can find
    """
    print(data["class"].loc[0])
    wins = possible_moves.loc[data[data.columns[9]]]
    return wins


def search(board):
    """
    search() performs a search of a given board for the best possible move

    :param board:
    :return: (row, col) for best move
    """
    # Will handle search for best_move()
    # MAY BE MERGED WITH best_move()
    # should use data to determine best move
    # TODO: Implement search method (Alpha-Beta preferable)\
    possible = filter_chosen(board)
    wins = filter_wins(possible)
    print(wins)


    # print(possible_moves)
    return (0, 0)


def best_move(letter, board):
    # Should perform search to find best move
    # will then run best move
    move = search(board)

    return
