import numpy as np
import pandas as pd
import pickle
import json
import os
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error

def predict(path, X:pd.DataFrame, y:pd.DataFrame, seed:int=42):

    with open(path, 'rb') as f:
        model = pickle.load(f)
    
    cv = KFold(5, shuffle=True, random_state=seed)
    
    scores = cross_val_score(model, X, np.ravel(y.values), cv=cv)

    preds = model.predict(X)
    
    metrics = {
        'CV-R2':round(np.mean(scores),3),
        'RMSE':np.sqrt(mean_squared_error(y, preds))
    }

    print("Performance on Test Data:\n")
    print(f"{metrics}\n")
    if not os.path.isdir(r"metrics/"):
        os.mkdir("metrics")
    with open(r"metrics/regressor_metrics.json",'w') as result:
        result.write(json.dumps(metrics))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('m', help='Path to regression model')
    parser.add_argument('xtest', help='test data set')
    parser.add_argument('ytest', help='true values')
    
    args = parser.parse_args()

    X = pd.read_csv(args.xtest, index_col=False)
    Y = pd.read_csv(args.ytest, index_col=False)

    predict(args.m, X, Y)