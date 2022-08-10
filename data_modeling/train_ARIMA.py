import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import date
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
import pickle
import os

def Avg_Asking(
        X: pd.DataFrame
):
    """
    Returns dataframe with average asking price by month
    """
    df = X.copy().dropna()
    df['Month'] = pd.to_datetime(pd.to_datetime(df['posted_at']).dt.to_period('m').astype(str))
    df = df.sort_values(by=['Month'])
    df_avg_asking = pd.DataFrame(df.groupby('Month').mean()['Asking'])
    return df_avg_asking

def train_test_split(
        X: pd.DataFrame
):
    train = X.iloc[:len(X) - 12]
    test = X.iloc[len(X) - 12:]  # set one year(12 months) for testing

    return train, test

def Find_Best_SARIMAX(
        df: pd.DataFrame
):
    """
    Trains an ARIMA model to forecast the average asking price of a
    used sailboat.
    """

    warnings.filterwarnings("ignore")

    stepwise_fit = auto_arima(df, start_p=1, start_q=1,
                              max_p=3, max_q=3, m=12,
                              start_P=0, seasonal=True,
                              d=None, D=1, trace=True,
                              random_state=42,
                              error_action='ignore',  # we don't want to know if an order does not work
                              suppress_warnings=True,  # we don't want convergence warnings
                              stepwise=True)  # set to stepwise

    order = stepwise_fit.order
    seasonal_order = stepwise_fit.seasonal_order

    return order, seasonal_order

def train_SARIMAX(
    train: pd.DataFrame, test: pd.DataFrame, order: str, seasonal_order: str
):

    """
    train model on best fit
    """

    model = SARIMAX(train,
                    order=order,
                    seasonal_order=seasonal_order)
    result = model.fit(disp=0)

    start = len(train)
    end = len(train) + len(test) - 1

    # Predictions for one-year against the test set
    test_predictions = result.predict(start, end,
                                 typ='levels').rename("Predictions")

    test_metrics = {
        'RMSE': np.sqrt(mean_squared_error(test, test_predictions))
    }

    print("Performance on Test Data:\n")
    print(test_metrics)

    if not os.path.isdir(r"models/"):
        os.mkdir("models")

    with open(r"models/ARIMA_model.pkl", 'wb') as out:
        pickle.dump(result, out)

    train_name = 'SARIMAX_train'
    test_name = 'SARIMAX_test'

    if not os.path.isdir(r"data/"):
        os.mkdir("data")

    train.to_csv(f"data/{train_name}.csv", index=True)
    train.to_csv(f"data/{test_name}.csv", index=True)

    fc = result.forecast(len(test) + 12)  # add on year of projections onto test set

    #create new dataframe for forecasting one year into future
    df_fc = pd.DataFrame(fc[-12:])
    lst = [date(i.year + 1, i.month, i.day) for i in test.index]
    df_fc['Month'] = lst
    df_fc = df_fc.set_index('Month')

    #combine train and test set to original dataset for plot
    df_combined = pd.concat([train, test])

    #produce forecasting plot for one year
    plt.figure(figsize=(12, 5), dpi=100)
    plt.plot(df_combined, label='Original Avg Asking')
    plt.plot(df_fc, label='Forecasted Avg Asking')
    plt.title('Monthly Average Asking Price')
    plt.legend(loc='upper right', fontsize=8)
    plt.savefig('app/static/forecast.png')
    plt.savefig('forecast.png')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('f', type=str, help='raw csv file with headers')

    args = parser.parse_args()

    df = pd.read_csv(args.f)
    df_avg_asking = Avg_Asking(df)
    train, test = train_test_split(df_avg_asking)
    order, seasonal_order = Find_Best_SARIMAX(train)
    train_SARIMAX(train, test, order, seasonal_order)