import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

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

    # Create decision tree
    decider = DecisionTreeClassifier(criterion='entropy')
    decider = decider.fit(x_train, y_train)

    # Test
    train_test_split(x_train, y_train, test_size=0.3, random_state=1)
    tree.plot_tree(decider, class_names=["False", "True"], fontsize=5)
    plt.show()

    negative_test = np.array([2, 2, 1, 2, 1, 0, 1, 0, 0])
    positive_test = np.array([2, 2, 2, 1, 1, 0, 1, 0, 0])
    test_group = [negative_test, positive_test]
    y_pred = decider.predict(test_group)
    print(y_pred)


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
