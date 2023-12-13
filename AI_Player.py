import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


#references: https://www.kaggle.com/code/sripadkarthik/tick-tack-toe-with-90-accuracy
#https://github.com/cybercoder-naj/TicTacToeAI/blob/main/main.py?source=post_page-----bf6725ed44f9--------------------------------
#https://github.com/aaditkapoor/tic-tac-toe-ml-project/blob/master/tic-tac-toe.ipynb

class AI_Player:
    def __init__(self, enemy_token, self_token):
        # Define tokens for board
        self.empty_token = 0
        self.enemy_token = enemy_token
        self.self_token = self_token

    # Function to find the best move for the AI using minimax with alpha-beta pruning
    def find_best_move(self, board):
        best_val = float('-inf')
        best_move = None

        empty_cells = self.get_empty_cells(board)

        for cell in empty_cells:
            board[cell[0]][cell[1]] = self.self_token
            move_val = self.minimax(board, 0, False, float('-inf'), float('inf'))
            board[cell[0]][cell[1]] = self.empty_token
            if move_val > best_val:
                best_move = cell
                best_val = move_val
        print(f"BEST MOVE: {best_move}")
        board[best_move[0]][best_move[1]] = self.self_token
        return board

    # Minimax function with alpha-beta pruning
    def minimax(self, board, depth, maximizing_player, alpha, beta):
        score = self.evaluate(board)

        if score is not None:
            return score

        empty_cells = self.get_empty_cells(board)

        if maximizing_player:
            max_eval = float('-inf')
            for cell in empty_cells:
                board[cell[0]][cell[1]] = self.self_token
                eval = self.minimax(board, depth + 1, False, alpha, beta)
                board[cell[0]][cell[1]] = self.empty_token
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for cell in empty_cells:
                board[cell[0]][cell[1]] = self.enemy_token
                eval = self.minimax(board, depth + 1, True, alpha, beta)
                board[cell[0]][cell[1]] = self.empty_token
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    # Function to get all empty cells on the board
    def get_empty_cells(self, board):
        return [(i, j) for i in range(len(board[0])) for j in range(len(board[0])) if board[i][j] == self.empty_token]

    # Function to evaluate the current state of the board
    def evaluate(self, board):
        if self.is_winner(board, self.self_token):
            return 1
        elif self.is_winner(board, self.enemy_token):
            return -1
        elif self.is_full(board):
            return 0
        else:
            return None

    # Function to check if the board is full
    def is_full(self, board):
        return all(board[i][j] != self.empty_token for i in range(len(board[0])) for j in range(len(board[0])))

    # Function to check if a player has won
    def is_winner(self, board, player):
        results = {self.check_rows(board), self.check_columns(board), self.check_diagonals(board)}
        if player in results:
            return True
        return False

    def check_rows(self, board):
        """
        check_rows() determines if a horizontal win has been found

        :return: X or O if winner found, empty string otherwise
        """

        # If all strings in row are the same
        for row in board:
            if len(set(row)) == 1 and row[0] != self.empty_token:
                return row[0]
        return ""

    def check_columns(self, board):
        """
        check_columns() determines if a vertical win has been found

        :return: X or O if winner found, empty string otherwise
        """

        # if all strings in col are the same
        for col in range(len(board[0])):
            column = []
            for item in range(len(board[0])):
                column.append(board[item][col])
            if len(set(column)) == 1 and board[0][col] != self.empty_token:
                return board[0][col]
        return ""

    def check_diagonals(self, board):
        """
        check_diagonals() determines if a diagonal win has been found

        :return: X or O if winner found, empty string otherwise
        """

        # if all strings in either diagonal are the same
        check = True
        check_2 = True
        for item in range(len(board[0])):
            # Left to Right
            if not (board[0][0] == board[len(board[0]) - 1 - item][len(board[0]) - 1 - item] and
                    board[0][0] != self.empty_token):
                check = False

            # Right To Left
            if not (board[0][len(board[0]) - 1] == board[len(board[0]) - 1 - item][0 + item] and
                    board[0][len(board[0]) - 1] != self.empty_token):
                check_2 = False
        if check:
            return board[0][0]
        if check_2:
            return board[0][len(board[0]) - 1]
        return ""
