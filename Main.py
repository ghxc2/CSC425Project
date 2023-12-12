"""
Main Script for AI Tic-Tac-Toe Player

This script will be the main script for controlling the tic-tac-toe game
May have GUI support eventually but for now is CLI
"""
import numpy as np
from AI_Player import AI_Player
import Winner
import GUI


class TicTacToeGame:
    def __init__(self, player_1, player_1_letter, player_2, player_2_letter):
        temp_board = np.zeros((3, 3), dtype=int)
        self.board = np.array(temp_board)
        self.player_1 = player_1
        self.player_1_letter = player_1_letter
        self.player_2 = player_2
        self.player_2_letter = player_2_letter
        self.empty_token = 0
        self.running = True
        self.current_player = 1
        self.winner = ""
        self.incorrect_win_finds = 0
        self.win_finds = 0

    def print_board(self):
        for row in self.board:
            print(" ".join(map(str, row)).replace("2", "x").replace("1", "o").replace("0", "_"))
        print()

    def claim_spot(self, row: int, col: int, token):
        """
        claim_spot will set a given spot to the letter passed
        as an argument, claiming that spot for that player

        :param row: row number of spot
        :param col: column number of spot
        :param letter: letter to place
        """
        self.board[row - 1][col - 1] = token
    def check_spot_availability(self, row: int, col: int):
        """
        check_spot_availability will determine if a spot is open

        :param row: row number of spot
        :param col: column number of spot
        :return: True if available, False if taken
        """
        return self.board[row - 1][col - 1] == self.empty_token

    def check_rows(self):
        """
        check_rows() determines if a horizontal win has been found

        :return: X or O if winner found, empty string otherwise
        """

        # If all strings in row are the same
        for row in self.board:
            if len(set(row)) == 1 and row[0] != self.empty_token:
                return row[0]
        return ""

    def check_columns(self):
        """
        check_columns() determines if a vertical win has been found

        :return: X or O if winner found, empty string otherwise
        """

        # if all strings in col are the same
        for col in range(3):
            column = [self.board[0][col], self.board[1][col], self.board[2][col]]
            if len(set(column)) == 1 and self.board[0][col] != self.empty_token:
                return self.board[0][col]
        return ""

    def check_diagonals(self):
        """
        check_diagonals() determines if a diagonal win has been found

        :return: X or O if winner found, empty string otherwise
        """

        # if all strings in either diagonal are the same
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[1][1] != self.empty_token)\
                or (self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[1][1] != self.empty_token):
            return self.board[1][1]
        return ""

    def check_board(self):
        """
        check_board determines if the game has finished
        and will set running to false if the game is over
        :return: empty string if running, X or O if win is found
        """

        # Check if a winner has been found

        # Check if a match 3 has been met
        rows = self.check_rows()
        cols = self.check_columns()
        diagonals = self.check_diagonals()
        # If winner found, set winner and return
        if rows != "":
            self.winner = rows
        elif cols != "":
            self.winner = cols
        elif diagonals != "":
            self.winner = diagonals
        if self.winner != "":
            self.running = False
            return
        decision_tree_win = Winner.find_win(self.board)

        # Incrememnt win finds to compare for later
        if not self.running:
            self.win_finds += 1
            if not decision_tree_win:
                self.incorrect_win_finds += 1
        if self.running and decision_tree_win:
            self.incorrect_win_finds += 1

        # Check if the board has filled
        empty_check = True
        for row in self.board:
            for item in row:
                if empty_check and item == self.empty_token:
                    empty_check = False
        if empty_check:
            self.running = False

    def get_user_turn(self, letter):
        """
        get_user_turn() Asks users where they would like to play their turn
        and plays them accordingly

        :param letter: letter of player to be placed when spot found
        """

        print("Please Enter Coordinates")
        while True:
            row = int(input("Please Enter Row Number: "))
            col = int(input("Please Enter Column Number: "))
            valid = self.check_spot_availability(row, col)
            if row not in (1, 2, 3) or col not in (1, 2, 3):
                valid = False
                print("Please Enter Valid Coordinates (1 - 3)")
            if valid:
                self.claim_spot(row, col, letter)
                return
            else:
                print("Taken, Please Enter Coordinates")

    def turn(self):
        """
        turn() processes the turn for the current player
        processing the move made by the next player
        doing so depending on whether the player
        is person or AI player
        """
        # Determine which player is taking their turn
        if self.current_player == 1:
            player = self.player_1
            player_letter = self.player_1_letter
        else:
            player = self.player_2
            player_letter = self.player_2_letter

        # Determine if player is CPU and move as such
        if isinstance(player, AI_Player):
            # Allow CPU to move
            print("AI Is moving")
            board = player.find_best_move(self.board)

        else:
            # Allow User to move
            self.get_user_turn(player_letter)

    def play(self):
        # Should continue until game is won
        # or until no available spaces
        while self.running:
            self.print_board()
            self.turn()
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1

            self.check_board()

        self.print_board()
        if self.winner == "":
            print("Draw")
        else:
            print(f"{self.winner} Wins!")
        print(f"False Found Wins: {self.incorrect_win_finds}")
        return


def choose_game():
    type = 0
    while type not in {1, 2, 3}:
        print("Please Select Game Type to Play:")
        print("1. Player v AI")
        print("2. AI v AI Normal")
        print("3. AI v AI Loop")
        type = int(input("Select (1, 2, 3): "))

    # Set Up Type
    if type == 1:
        print("Please Select Player Info: ")
        char = ""
        while char.lower() not in {"x", "o"}:
            char = str(input("x or o: "))

        # Convert to number for game to be able to play
        number = 0
        if char == "x":
            number = 2
        else:
            number = 1

        ai_char = 0
        if char.lower() == "x":
            ai_char = 1
        else:
           ai_char = 2

        turn = 0
        while turn not in {1, 2}:
            turn = int(input("Player Goes First or Second (1, 2): "))

        # Create Game
        game = None
        if turn == 1:
            game = TicTacToeGame("Player", number, AI_Player(number, ai_char), ai_char)
        else:
            game = TicTacToeGame(AI_Player(number, ai_char), ai_char, "Player", number)
        game.play()
    elif type == 2:
        game = TicTacToeGame(AI_Player(2, 1), 1, AI_Player(1, 2), 2)
        game.play()
    elif type == 3:
        game = TicTacToeGame(AI_Player(2, 1), 1, AI_Player(1, 2), 2)
        iterations = 0
        while iterations <= 0:
            iterations = int(input("Number Of Games To Play: "))
        play_loop(game, iterations)


def play_loop(game, iterations):
    results = [0, 0, 0]
    total_false_wins = 0
    for i in range(iterations):
        win, false_wins = game.winner, game.incorrect_win_finds
        total_false_wins += false_wins
        if win == "":
            results[0] += 1
        elif win == "x":
            results[1] += 1
        elif win == "o":
            results[2] += 1
    print(f"Draws: {results[0]}")
    print(f"X Wins: {results[1]}")
    print(f"O Wins: {results[2]}")
    print(f"Overall False Wins: {total_false_wins}")


if __name__ == "__main__":
    Winner.init()
    choose_game()
