from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
import numpy as np


def train_ridge(x_matrix, y_matrix, alpha):
    model = Ridge(alpha=alpha).fit(x_matrix, y_matrix)

    # print cross validation score
    score = cross_val_score(model, x_matrix, y_matrix, cv=10).mean()


    # return trained model
    return model, score
