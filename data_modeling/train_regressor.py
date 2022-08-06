import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold
import pickle
import os
import joblib

def train_regression_model(
    X: pd.DataFrame, y: str, seed: int=42
):
    """
    Trains a linear model to predict the asking price of a 
    used sailboat given sailboat features.
    """

    print() # f"{len(y)} records in the training set.\n"

    cv = KFold(5, shuffle=True, random_state=seed)

    pipe = Pipeline([
        ('scaler', StandardScaler()), ('model', RandomForestRegressor(n_estimators=300,random_state=seed))
    ])

    pipe.fit(X, np.ravel(y.values))
    train_scores = cross_val_score(pipe, X, np.ravel(y.values), cv=cv)

    metrics = {
        'CV-R2': round(np.mean(train_scores), 3),
        'RMSE': np.sqrt(mean_squared_error(y, pipe.predict(X)))
    }
    print("Performance on Training Data:\n")
    print(f"{metrics}\n")

    if not os.path.isdir(r"models/"):
        os.mkdir("models")

    joblib.dump(pipe, 'models/regression_model' + '.compressed', compress=True)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('xtrain', help='data\X_train.csv')
    parser.add_argument('ytrain', help='data\y_train.csv')
    
    args = parser.parse_args()

    X_TRAIN = pd.read_csv(args.xtrain, index_col=False)
    Y_TRAIN = pd.read_csv(args.ytrain, index_col=False)

    train_regression_model(X_TRAIN, Y_TRAIN)