"""
Main Script for AI Tic-Tac-Toe Player

This script will be the main script for controlling the tic-tac-toe game
May have GUI support eventually but for now is CLI
"""
import numpy as np
import AI_Player
board = [["","",""],["","",""],["","",""]]
board = np.array(board)
player_1 = "User"
player_1_letter = "X"
player_2 = "CPU"
player_2_letter = "O"
running = True
current_player = 1
winner = ""


def print_board():
    # Make pretty eventually
    for row in board:
        print(row[0] + " | " + row[1] + " | " + row[2])
        print("------------")


def claim_spot(row: int, col: int, letter):
    """
    claim_spot will set a given spot to the letter passed
    as an argument, claiming that spot for that player

    :param row: row number of spot
    :param col: column number of spot
    :param letter: letter to place
    """
    board[row - 1][col - 1] = letter


def check_spot_availability(row: int, col: int):
    """
    check_spot_availability will determine if a spot is open

    :param row: row number of spot
    :param col: column number of spot
    :return: True if available, False if taken
    """
    return board[row - 1][col - 1] == ""


def choose_letter():
    # Do later, for now player goes first and is X
    # TODO: Should allow player to choose X or O
    # TODO: Should allow player to go first or second
    # TODO: Possibly allow player to have 2 AIs fight
    return


def check_rows():
    """
    check_rows() determines if a horizontal win has been found

    :return: X or O if winner found, empty string otherwise
    """

    # If all strings in row are the same
    for row in board:
        if len(set(row)) == 1 and row[0] != "":
            return row[0]
    return ""


def check_columns():
    """
    check_columns() determines if a vertical win has been found

    :return: X or O if winner found, empty string otherwise
    """

    # if all strings in col are the same
    for col in range(3):
        column = [board[0][col], board[1][col], board[2][col]]
        if len(set(column)) == 1 and board[0][col] != "":
            return board[0][col]
    return ""


def check_diagonals():
    """
    check_diagonals() determines if a diagonal win has been found

    :return: X or O if winner found, empty string otherwise
    """

    # if all strings in either diagonal are the same
    if (board[0][0] == board[1][1] == board[2][2] and board[1][1] != "")\
            or (board[0][2] == board[1][1] == board[2][0] and board[1][1] != ""):
        return board[1][1]
    return ""


def check_board():
    """
    check_board determines if the game has finished
    and will set running to false if the game is over
    :return: empty string if running, X or O if win is found
    """
    global winner
    global running

    # Check if a winner has been found

    # Check if a match 3 has been met
    rows = check_rows()
    cols = check_columns()
    diagonals = check_diagonals()
    # If winner found, set winner and return
    if rows != "":
        winner = rows
    elif cols != "":
        winner = cols
    elif diagonals != "":
        winner = diagonals
    if winner != "":
        running = False
        return

    # Check if the board has filled
    empty_check = True
    for row in board:
        for item in row:
            if empty_check and item == "":
                empty_check = False
    if empty_check:
        running = False






def get_user_turn(letter):
    """
    get_user_turn() Asks users where they would like to play their turn
    and plays them accordingly

    :param letter: letter of player to be placed when spot found
    """

    print("Please Enter Coordinates")
    while True:
        row = int(input("Please Enter Row Number: "))
        col = int(input("Please Enter Column Number: "))
        valid = check_spot_availability(row, col)
        if row not in (1, 2, 3) or col not in (1, 2, 3):
            valid = False
            print("Please Enter Valid Coordinates (1 - 3)")
        if valid:
            claim_spot(row, col, letter)
            return
        else:
            print("Taken, Please Enter Coordinates")
def turn():
    """
    turn() processes the turn for the current player
    processing the move made by the next player
    doing so depending on whether the player
    is person or AI player
    """

    # Determine which player is taking their turn
    if current_player == 1:
        player = player_1
        player_letter = player_1_letter
    else:
        player = player_2
        player_letter = player_2_letter

    # Determine if player is CPU and move as such
    if player == "CPU":
        # Allow CPU to move
        AI_Player.best_move("O", board)
    else:
        # Allow User to move
        get_user_turn(player_letter)


def play():
    # Should continue until game is won
    # or until no available spaces
    global current_player
    while running:
        turn()
        print_board()
        if current_player == 1:
            current_player = 2
        else:

            current_player = 1

        check_board()


    if winner == "":
        print("Draw")
    else:
        print(winner + " Wins!")
    return


play()
