from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedKFold
import numpy as np


def train_ridge(x_matrix, y_matrix):
    model = Ridge()

    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)

    grid = dict()
    grid['alpha'] = np.arange(0, 1, 0.01)

    # define search
    search = GridSearchCV(model, grid, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)

    results = search.fit(x_matrix, y_matrix)

    # summarize
    print('MAE: %.3f' % results.best_score_)
    print('Config: %s' % results.best_params_)

    return results
