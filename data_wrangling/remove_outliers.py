import argparse
import pandas as pd
import os

def remove_outliers(df: pd.DataFrame,
                    columns:list = ['Length', 'Beam', 'Draft', 'Year', 'Asking_Price_Adj'],
                    multiplier: float = 1.5
                    ) -> pd.DataFrame:
    """
    Removes outlier events which are outside of the inter quartile ranges.
    https://medium.com/analytics-vidhya/removing-outliers-understanding-how-and-what-behind-the-magic-18a78ab480ff
    """

    df_2 = df.copy(deep=True)
    outliers = []
    for col in columns:
        q1 = df_2[col].quantile(0.25)
        q3 = df_2[col].quantile(0.75)
        iqr = q3-q1
        lower_limit = q1 - multiplier * iqr
        upper_limit = q3 + multiplier * iqr

        is_outlier = lambda x: 1 if (x < lower_limit) | (x > upper_limit) else 0
        df_2['is_outlier'] = df_2[col].map(is_outlier)

        outliers.extend(df_2[df_2['is_outlier']==1].index.to_list())

    df.drop(index=outliers, inplace=True)

    return df, outliers

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Removes outliers by IQR')
    parser.add_argument('input_file', help='intermediates/listings.csv')
    parser.add_argument('output_file', help='./data/listings_wo_outliers.csv')
    parser.add_argument('-m', type=float, default=1.5, help='IQR multiplier')

    args = parser.parse_args()

    df_in = pd.read_csv(args.input_file)
    df_out, outliers = remove_outliers(df_in, multiplier=args.m)

    os.makedirs(r"./data", exist_ok=True)
    df_out.to_csv(args.output_file, index=False)
