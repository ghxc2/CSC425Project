"""
Main Script for AI Tic-Tac-Toe Player

This script will be the main script for controlling the tic-tac-toe game
"""
import numpy as np
from AI_Player import AI_Player
import Winner


class TicTacToeGame:
    def __init__(self, player_1, player_1_letter, player_2, player_2_letter, size):
        self.size = size
        temp_board = np.zeros((size, size), dtype=int)
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

    def reset(self):
        temp_board = np.zeros((self.size, self.size), dtype=int)
        self.board = np.array(temp_board)
        self.running = True
        self.current_player = 1
        self.winner = ""
        self.incorrect_win_finds = 0
        self.win_finds = 0

    def print_board(self):
        for row in self.board:
            print(self.char_fix(" ".join(map(str, row))))
        print()

    @staticmethod
    def char_fix(string):
        return str(string).replace("2", "x").replace("1", "o").replace("0", "_")

    def claim_spot(self, row: int, col: int, token):
        """
        claim_spot will set a given spot to the letter passed
        as an argument, claiming that spot for that player

        :param row: row number of spot
        :param col: column number of spot
        :param token: letter to place
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
        for col in range(self.size):
            column = []
            for item in range(self.size):
                column.append(self.board[item][col])
            if len(set(column)) == 1 and self.board[0][col] != self.empty_token:
                return self.board[0][col]
        return ""

    def check_diagonals(self):
        """
        check_diagonals() determines if a diagonal win has been found

        :return: X or O if winner found, empty string otherwise
        """

        # if all strings in either diagonal are the same
        check = True
        check_2 = True
        for item in range(self.size):
            # Left to Right
            if not (self.board[0][0] == self.board[self.size - 1 - item][self.size - 1 - item] and
                    self.board[0][0] != self.empty_token):
                check = False

            # Right To Left
            if not (self.board[0][self.size - 1] == self.board[self.size - 1 - item][0 + item] and
                    self.board[0][self.size - 1] != self.empty_token):
                check_2 = False
        if check:
            return self.board[0][0]
        if check_2:
            return self.board[0][self.size - 1]
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

        # Does not work in bigger than 3 area!
        if self.size == 3:
            decision_tree_win = Winner.find_win(self.board)

        # Incrememnt win finds to compare for later
        if not self.running:
            self.win_finds += 1
            if self.size == 3:
                if not decision_tree_win:
                    self.incorrect_win_finds += 1
        if self.size == 3:
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
            valid_choices = range(self.size + 1)[1:]
            if row not in valid_choices or col not in valid_choices:
                valid = False
                print(f"Please Enter Valid Coordinates (1 - {self.size})")
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
            self.board = player.find_best_move(self.board)

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
            print(f"{self.char_fix(self.winner)} Wins!")
        if self.size == 3:
            print(f"False Found Wins: {self.incorrect_win_finds}")
        return

class TicTacToeWrapper:
    def __init__(self, player_1, player_2, size):
        self.results = [0, 0, 0]
        self.total_false_wins = 0
        self.players = (player_1, player_2)
        self.game = None
        self.size = size
        self.iterations = 1
        self.make()

    def make(self):
        if self.players[0].number == 1:
            self.game = TicTacToeGame(self.players[0].player, self.players[0].player_token, self.players[1].player,
                                      self.players[1].player_token, self.size)
        else:
            self.game = TicTacToeGame(self.players[1].player, self.players[1].player_token, self.players[0].player,
                                      self.players[0].player_token, self.size)

    def play(self):
        if self.iterations == 1:
            self.game.play()
        else:
            self.play_loop()

    def play_loop(self):
        for i in range(self.iterations):
            self.game.reset()
            self.game.play()
            win, false_wins = self.game.winner, self.game.incorrect_win_finds
            self.total_false_wins += false_wins
            if win == "":
                self.results[0] += 1
            elif win == "x":
                self.results[1] += 1
            elif win == "o":
                self.results[2] += 1
        print(f"Draws: {self.results[0]}")
        print(f"X Wins: {self.results[1]}")
        print(f"O Wins: {self.results[2]}")
        if self.game.size == 3:
            print(f"Overall False Wins: {self.total_false_wins}")


class Player:
    def __init__(self, player, player_token, number):
        self.player = player
        self.player_token = player_token
        self.number = number


def choose_game():
    game_type = 0
    while game_type not in {1, 2, 3}:
        print("Please Select Game Type to Play:")
        print("1. Player v AI")
        print("2. AI v AI Normal")
        print("3. AI v AI Loop")
        game_type = int(input("Select (1, 2, 3): "))
    size = 0
    while size <= 0:
        size = int(input("Enter Board Size: "))
    wrapper = None
    # Set Up Type
    if game_type == 1:
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

        # Create Players
        ai_turn = [item for item in range(3) if (item > 0 and item != turn)]
        player_ai = Player(AI_Player(number, ai_char), ai_char, ai_turn[0])
        player = Player("Player", number, turn)

        # Create Game
        wrapper = TicTacToeWrapper(player_ai, player, size)
    elif game_type == 2 or game_type == 3:
        player_ai = Player(AI_Player(2, 1), 1, 1)
        player_ai_2 = Player(AI_Player(1, 2), 2, 2)
        wrapper = TicTacToeWrapper(player_ai, player_ai_2, size)
        if game_type == 3:

            iterations = 0
            while iterations <= 0:
                iterations = int(input("Number Of Games To Play: "))
            wrapper.iterations = iterations
    return wrapper


if __name__ == "__main__":
    Winner.init()
    wrapper = choose_game()
    wrapper.play()
