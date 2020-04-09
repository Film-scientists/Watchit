"""
Adjusting algorithm
-------------------
The following program will check the best values for the SVD algorithm,
which is a matrix factorization algorithm
"""
import pandas as pd
from surprise import Reader
from surprise import SVD, Dataset
from surprise.model_selection import GridSearchCV

reader = Reader(rating_scale=(0, 10))

# Small rating base
rating = {
    "item": [1, 2, 1, 2, 1, 2, 1, 2, 1],
    "user": ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E'],
    "rating": [6, 2, 5, 4, 2.5, 9, 4.5, 7, 9]}

df = pd.DataFrame.from_dict(rating)                                         # Convert to DataFrame
data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)         # Load data into Dataset
param_grid = {
    "n_epochs": [5, 10, 7],                 # Number of iterations in SGD
    "lr_all": [0.002, 0.005, 0.003],        # Learning rate for all parameters
    "reg_all": [0.4, 0.6, 0.2]}             # regularization term for all parameters

gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)
# cv - n-fold cross-validation procedure
# In this case 3-fold
# rmse - root-mean-square error
# mea - mean absolute error

gs.fit(data)

# Show the best score
print(gs.best_score["rmse"])

# Parameters associated with the best score
print(gs.best_params["rmse"])
