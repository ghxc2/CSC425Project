import tkinter as tk
from tkinter import ttk
from Main import TicTacToeGame, Player, TicTacToeWrapper
from AI_Player import AI_Player
import Winner
"""
UNUSED
REQUIRED REWRITING ENTIRE GAME SYSTEM
DEEMED UNNECCESARY
"""
# references: https://www.geeksforgeeks.org/python-grid-method-in-tkinter/
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight= 1)
        self.game_size = 0
        self.game_wrapper = None
        self.player_token = ""
        start_frame = Start(self.container, self)
        start_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(start_frame)

    def show_frame(self, frame):
        frame.tkraise()

    def generate_game_frame(self):
        game_frame = GameFrame(self.container, self)
        self.show_frame(game_frame)

    def move(self, i, j):
        self.game_wrapper.game.get_user_turn(i, j, self.player_token)
class Start(tk.Frame):
    def __init__(self, parent, controller):
        # Create Start Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="TicTacToe Player")
        label.pack()
        # Select Type of Game To Play
        label_type = ttk.Label(self, text="Please Select Game Type to Play:")
        label_type.pack()
        self.types = ["Player v AI", "AI v AI Normal", "AI v AI Loop"]
        self.combo_type = ttk.Combobox(
            self,
            state="readonly",
            values=self.types
        )
        self.combo_type.pack()

        # Enter Board Size
        label_size = ttk.Label(self, text="Enter Board Size: ")
        label_size.pack()
        self.entry_size = ttk.Entry(self)
        self.entry_size.pack()

        # Error Spot
        self.label_error = ttk.Label(self, text="")
        self.label_error.pack()
        # Enter Button
        self.enter_button = ttk.Button(self, text="Enter", command=self.checker)
        self.enter_button.pack()
    def checker(self):
        size = 0
        error = ""
        try:
            size = int(self.entry_size.get())
        except ValueError:
            size = -1
        if size <= 0:
            error += "Please Enter a Number Greater than 0\n"
        if self.combo_type.get() == "":
            error += "Please Select Game Type\n"

        self.label_error.config(text=error)
        if error == "":

            game_type = self.types.index(self.combo_type.get())
            self.controller.game_size = size
            if game_type == 0:
                self.player_creator()
            if game_type == 1:
                self.ai_game()
            if game_type == 2:
                self.loop_creator()

    def player_creator(self):
        # Player Info
        label_player = tk.Label(self, text="Please Select Player Info")
        label_player.pack()

        # Token Selection
        label_token = tk.Label(self, text="x or o")
        label_token.pack()
        self.tokens = ["o", "x"]
        self.combo_char = ttk.Combobox(
            self,
            state="readonly",
            values=self.tokens
        )
        self.combo_char.pack()

        # Turn selection
        label_turn = tk.Label(self, text="Player Goes First or Second")
        label_turn.pack()
        self.turns = ["First", "Second"]
        self.combo_turns = ttk.Combobox(
            self,
            state="readonly",
            values=self.turns
        )
        self.combo_turns.pack()

        # Player Error
        self.label_player_error = tk.Label(self, text="")
        self.label_player_error.pack()

        # Player Button
        player_button = tk.Button(self, text="Start", command=self.player_checker)
        player_button.pack()

    def player_checker(self):
        error = ""
        if self.combo_char.get() == "":
            error += "Please Select x or o\n"
        if self.combo_turns == "":
            error += "Please Select First or Second\n"
        self.label_player_error.config(text=error)

        # Valid Player
        if error == "":
            char = self.tokens.index(self.combo_char.get()) + 1
            turn = self.turns.index(self.combo_turns.get()) + 1
            self.controller.player_token = char
            self.player_game(char, turn)

    def loop_creator(self):
        # Iterations Info
        self.label_iterations = tk.Label(self, text="Please Enter Iterations to Play")
        self.label_iterations.pack()
        self.entry_iterations = tk.Entry(self)
        self.entry_iterations.pack()

        # Iterations error
        self.label_iterations_error = tk.Label(self, text="")
        self.label_iterations_error.pack()

        # Iterations Button
        iter_button = tk.Button(self, text="Start", command=self.loop_checker)
        iter_button.pack()

    def loop_checker(self):
        # Ensure valid iterations
        iterations = 0
        error = ""
        try:
            iterations = int(self.entry_iterations.get())
        except ValueError:
            iterations = -1
        if iterations <= 0:
            error += "Please Enter Iterations Larger than 0"
        self.label_iterations_error.config(text=error)

        # Valid iterations
        if error == "":
            self.ai_game()
            self.controller.game_wrapper.iterations = iterations

    def ai_game(self):
        player_ai = Player(AI_Player(2, 1), 1, 1)
        player_ai_2 = Player(AI_Player(1, 2), 2, 2)
        self.controller.game_wrapper = TicTacToeWrapper(player_ai, player_ai_2, self.controller.game_size)
        self.controller.generate_game_frame()


    def player_game(self, token, turn):
        player = Player("Player", token, turn)
        ai_turn = [item for item in range(3) if (item > 0 and item != turn)]
        ai_char = [item for item in range(3) if (item > 0 and item != token)]
        player_ai = Player(AI_Player(token, ai_char), ai_char, ai_turn[0])
        self.controller.game_wrapper = TicTacToeWrapper(player, player_ai, self.controller.game_size)
        self.controller.generate_game_frame()


class GameFrame(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        for i in range(controller.game_size):
            for j in range(controller.game_size):
                button = tk.Button(self, text="_", command=lambda : self.try_turn(button, i, j))
                self.update_button(button, i, j)
    def try_turn(self, button, i, j):
        if self.get_game_token() == "_":
            x = True
    def update_button(self, button, i, j):
        text = self.get_game_token(i, j)
        button.configure(text=text)
        root.after(1000, self.update, button, i, j)

    def get_game_token(self, i, j):
        return self.controller.game_wrapper.board[i][j]



root = App()
Winner.init()
root.mainloop()
