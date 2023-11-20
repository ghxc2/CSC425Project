import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


#references: https://www.kaggle.com/code/sripadkarthik/tick-tack-toe-with-90-accuracy
#https://github.com/cybercoder-naj/TicTacToeAI/blob/main/main.py?source=post_page-----bf6725ed44f9--------------------------------
#https://github.com/aaditkapoor/tic-tac-toe-ml-project/blob/master/tic-tac-toe.ipynb


# Constants for the Tic Tac Toe board
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2

# Function to convert 'x', 'o', 'b' to numerical values
def convert_to_numeric(value):
    if value == 'x':
        return PLAYER_X
    elif value == 'o':
        return PLAYER_O
    else:
        return EMPTY

# Function to print the Tic Tac Toe board
def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))
    print()

# Function to check if a player has won
def is_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Function to check if the board is full
def is_full(board):
    return all(board[i][j] != EMPTY for i in range(3) for j in range(3))

# Function to evaluate the current state of the board
def evaluate(board):
    if is_winner(board, PLAYER_X):
        return 1
    elif is_winner(board, PLAYER_O):
        return -1
    elif is_full(board):
        return 0
    else:
        return None

# Function to get all empty cells on the board
def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

# Minimax function with alpha-beta pruning
def minimax(board, depth, maximizing_player, alpha, beta):
    score = evaluate(board)

    if score is not None:
        return score

    empty_cells = get_empty_cells(board)

    if maximizing_player:
        max_eval = float('-inf')
        for cell in empty_cells:
            board[cell[0]][cell[1]] = PLAYER_X
            eval = minimax(board, depth + 1, False, alpha, beta)
            board[cell[0]][cell[1]] = EMPTY
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for cell in empty_cells:
            board[cell[0]][cell[1]] = PLAYER_O
            eval = minimax(board, depth + 1, True, alpha, beta)
            board[cell[0]][cell[1]] = EMPTY
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to find the best move for the AI using minimax with alpha-beta pruning
def find_best_move(board):
    best_val = float('-inf')
    best_move = None

    empty_cells = get_empty_cells(board)

    for cell in empty_cells:
        board[cell[0]][cell[1]] = PLAYER_X
        move_val = minimax(board, 0, False, float('-inf'), float('inf'))
        board[cell[0]][cell[1]] = EMPTY

        if move_val > best_val:
            best_move = cell
            best_val = move_val

    return best_move

# Function to play the game with AI using minimax with alpha-beta pruning
def ai_player(model):
    board = np.zeros((3, 3), dtype=int)

    while True:
        print_board(board)

        # Player's move
        while True:
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
            if board[row][col] == EMPTY:
                break
            else:
                print("Invalid move. Cell already occupied. Try again.")
        board[row][col] = PLAYER_O

        # Check if the player wins
        if is_winner(board, PLAYER_O):
            print("Player wins!")
            break

        # Check if draw
        if is_full(board):
            print("Draw")
            break

        print_board(board)

        # AI's move using minimax with alpha-beta pruning
        ai_move = find_best_move(board)
        print(f"AI chooses: {ai_move}")
        board[ai_move[0]][ai_move[1]] = PLAYER_X

        # Check if the AI wins
        if is_winner(board, PLAYER_X):
            print("AI wins!")
            break

        # Check if draw
        if is_full(board):
            print("Draw")
            break

if __name__ == "__main__":

    csv_file_path = "tic-tac-toe.csv"

    # Read the dataset from the CSV file
    dataset = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            board = [convert_to_numeric(row[key]) for key in ["TL", "TM", "TR", "ML", "MM", "MR", "BL", "BM", "BR"]]
            label = int(row["class"] == 'true')
            dataset.append((board, label))

    # Split the dataset into features (X) and labels (y)
    X = [data[0] for data in dataset]
    y = [data[1] for data in dataset]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a decision tree classifier
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model on the testing set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Play the game with AI using minimax with alpha-beta pruning
    ai_player(model)
