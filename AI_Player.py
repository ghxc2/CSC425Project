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
        return [(i, j) for i in range(3) for j in range(3) if board[i][j] == self.empty_token]

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
        return all(board[i][j] != self.empty_token for i in range(3) for j in range(3))

    # Function to check if a player has won
    def is_winner(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
                    all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or \
                all(board[i][2 - i] == player for i in range(3)):
            return True
        return False
