from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
import numpy as np

def train_regression(x_matrix, y_matrix):
    trained_model = LinearRegression().fit(x_matrix, y_matrix)
    # What does this function do ? #
    cross_score = cross_val_score(trained_model, x_matrix, y_matrix, cv=10).mean()
    print(cross_score)
    y_predicted = trained_model.predict(x_matrix)
    rmse = mean_squared_error(y_matrix, y_predicted)
    print(rmse)
    r2 = r2_score(y_matrix, y_predicted)
    print(r2)

    return trained_model

def train_regression_ridge(x_matrix, y_matrix):
    regression = linear_model.RidgeCV(alphas=np.logspace(-6, 6, 13))
    reg.fit()