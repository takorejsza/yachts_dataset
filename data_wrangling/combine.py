import os
import pandas as pd

def combine(df1, df2):

    # get the raw_listings dataset
    df1 = df1.drop(columns=['Unnamed: 0'])
    df1= df1.rename(columns={'Asking: ':'Asking'})
    # get additional features dataset containing features like Rigging, Cabins and Conditions
    df2 = df2.drop(columns=['Unnamed: 0'])
    df2 = df2.rename(columns={'Price':'Asking'})
    
    # Merge two dataframes together
    combine = pd.merge(df1[['Model','posted_at','Asking','Engine: ']],df2,on=['Model','posted_at','Asking'])
    return combine


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file1', help='data_wrangling/intermediates/raw_listings.csv') 
    parser.add_argument('input_file2', help='data_wrangling/intermediates/additional_features_dataset.csv')
    parser.add_argument('output_file', help='data_wrangling/intermediates/raw_combined_dataset.csv')
    args = parser.parse_args()

    df1 = pd.read_csv(args.input_file1)
    df2 = pd.read_csv(args.input_file2)

    combined = combine(df1,df2)

    os.makedirs(r"data_wrangling/intermediates", exist_ok=True)
    combined.to_csv(args.output_file, index=False)