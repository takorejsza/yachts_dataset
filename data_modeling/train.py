import json
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, KFold, cross_val_score, cross_val_predict
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score,mean_squared_error
import matplotlib.pyplot as plt

def train(df):

    df = df.drop(columns=['Unnamed: 0'])
    
    # Drop off features with correlation below 0.1 
    df.drop(columns=["Material","Hull","Location","Motor_Type",'posted_at','Asking'], inplace=True)

    df['Is_Cruiser'] = df['Type'].map(lambda x: 1 if x == 'cruiser' else 0)
    df['Is_Daysailer'] = df['Type'].map(lambda x: 1 if x == 'daysailer' else 0)
    df.drop(columns=["Type"], inplace=True)

    # Split the dataset into train and test sets
    train, test = train_test_split(df, train_size = 0.80, test_size = 0.20,random_state=42)

    # Get X_train, y_train, X_test and y_test for modeling
    X_train= train.loc[:,train.columns != 'Asking_Price_Adj']
    y_train = train['Asking_Price_Adj']

    X_test= test.loc[:,test.columns != 'Asking_Price_Adj']
    y_test = test['Asking_Price_Adj']

    # According to the GridSearch result, the best regression classfier is RandomForestRegressor() and the best n_estimators is 300.
    model = make_pipeline(StandardScaler(),RandomForestRegressor(n_estimators=300, random_state=42))
    model.fit(X_train, y_train)
    
    metrics = {
        'train_data': {
            'score': r2_score(y_train, model.predict(X_train)),
            'rmse': np.sqrt(mean_squared_error(y_train, model.predict(X_train))),
        },
        'test_data': {
            'score': r2_score(y_test, model.predict(X_test)),
            'rmse': np.sqrt(mean_squared_error(y_test, model.predict(X_test))),
        },
    }
    
    return metrics, model


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='./data/dataset_wo_outliers.csv')
    parser.add_argument('output_file', help='data_modeling/trained_model.pkl')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='display metrics',
    )
    args = parser.parse_args()

    input_data = pd.read_csv(args.input_file)

    metrics, model = train(input_data)

    if args.verbose:
        print(json.dumps(metrics, indent=2))

    with open(args.output_file, 'wb+') as out:
        pickle.dump(model, out)