import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# ref https://www.kaggle.com/code/johndoea/tic-tac-toe-decision-tree

df = pd.read_csv("tic-tac-toe.csv")
decider = None


# Function to fix all values in table using .apply()
def fix_values(x):
    print(f"Changing: {x}")
    if x == "b":
        return 0
    if x == "x":
        return 2
    if x == "o":
        return 1
    if x:
        return 1
    else:
        return 0


def init():
    global decider
    # feature names
    features = df.columns[:-1]

    # Get information for training

    for col in df.columns:
        df[col] = df[col].apply(fix_values)
    x_train = df[features]
    y_train = df["class"]

    print(df)

    print(x_train)
    print(y_train)
    # Create decision tree
    decider = DecisionTreeClassifier(criterion='entropy')
    decider = decider.fit(x_train.values, y_train.values)


def find_win(board):
    global decider
    items = []
    for _ in board:
        for item in _:
            items.append(item)
    result = decider.predict([items])
    print(f"Items: {items}")
    print(f"Results: {result[0]}")
    if result[0] == 1:
        return True
    else:
        return False
