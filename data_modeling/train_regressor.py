import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score, KFold
import pickle
import os

def train_regression_model(
    X: pd.DataFrame, y: str, seed: int=7
):
    """
    Trains a linear model to predict the asking price of a 
    used sailboat given sailboat features.
    """

    print() # f"{len(y)} records in the training set.\n"

    cv = KFold(5, shuffle=True, random_state=seed)

    pipe = Pipeline([
        ('scaler', StandardScaler()), ('model', Ridge(alpha=5e-6))
    ])

    pipe.fit(X, y)
    train_scores = cross_val_score(pipe, X, y, cv=cv)

    metrics = {
        'CV-R2': round(np.mean(train_scores), 3),
        'RMSE': np.sqrt(mean_squared_error(y, pipe.predict(X)))
    }
    print("Performance on Training Data:\n")
    print(f"{metrics}\n")

    if not os.path.isdir(r"models/"):
        os.mkdir("models")
    
    with open(r"models/regression_model.pkl", 'wb') as out:
        pickle.dump(pipe, out)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('xtrain', help='data\X_train.csv')
    parser.add_argument('ytrain', help='data\y_train.csv')
    
    args = parser.parse_args()

    X_TRAIN = pd.read_csv(args.xtrain, index_col=False)
    Y_TRAIN = pd.read_csv(args.ytrain, index_col=False)

    train_regression_model(X_TRAIN, Y_TRAIN)