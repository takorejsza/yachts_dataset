import os
import argparse
import pandas as pd
import re
import cpi
from datetime import date

def adjust_for_inflation(df:pd.DataFrame) -> pd.DataFrame:
    cpi.update()

    def adjust(s):
        try:
            real_price = cpi.inflate(s['Asking'], s['Year_Listed'])
            return real_price
        except:
            return s['Asking']

    df['Asking_Price_Adj'] = df.apply(adjust, axis=1)
    return df

def clean_transform(file:str, drop_null:bool=True) -> pd.DataFrame:
    df = pd.read_csv(file, usecols=[i for i in range(1,12)])
    df.columns = [c.strip().replace(':','') for c in df.columns]

    "=======QUANTITATIVE VARIABLES======"
    df['posted_at'] = pd.to_datetime(df['posted_at'])
    money_func = lambda x: float(x.replace('$','').replace(',',''))
    df['Asking'] = df['Asking'].map(money_func)

    def format_func(f:str):
        try:
            return ".".join(re.split("[^0-9]",f)).rstrip('.').replace('..','.')
        except:
            return None

    for col in ['Length', 'Beam', 'Draft']:
        df[col] = pd.to_numeric(df[col].map(format_func), errors='coerce')

    """=======DUMMY / CATEGORICAL VARIABLES======"""

    df['Material'],\
    df['Hull_Type'] = zip(*df["Hull"].\
                            map(lambda string: tuple(string.split(u'\xa0'))))
    df['Is_Mono'] = df['Hull_Type'].map(lambda x: 1 if x == 'monohull' else 0)

    df.drop(columns=["Hull"], inplace=True)

    df["Type"] = df["Type"].astype(str)
    design_func = lambda t: 'racer' if re.search('racer',t) else t
    df["Type"] = df["Type"].map(design_func)

    yacht_classes = ('cruiser','daysailer', 'dingy', 'motorsailer', 'racer')
    df = df[df["Type"].isin(yacht_classes)]

    """=======CATEGORICAL ENCODING======"""

    df["Engine"] = df["Engine"].astype(str)
    diesel_check = lambda d: 1 if re.search('diesel', d) else 0
    df['Is_Diesel'] = df['Engine'].map(diesel_check)

    def motor_type(engine):
        if (engine == None) | (engine == 'nan'):
            return 'motorless'
        if re.search('^0', engine):
            return 'motorless'
        engine_details = engine.split(' ')
        if 'inboard' in engine_details:
            return 'inboard'
        elif 'outboard' in engine_details:
            return 'outboard'
        else:
            return None
    df['Motor_Type'] = df['Engine'].map(motor_type)

    """=======ORDINAL ENCODING======"""

    def engine_count(engine):
        engine_details = re.search("[0-9]+", engine)
        if engine_details:
            return int(engine_details.group(0))
        else:
            return 1

    df['Engine_Count'] = df['Engine'].map(engine_count)

    """=======CORRECT ISSUES CAUSED BY NON-STANDARD NOTATION======"""
    engf = lambda x : 0 if x['Motor_Type'] == 'motorless' else x['Engine_Count']
    df['Engine_Count'] = df.apply(engf, axis=1)
    dslf = lambda x : 0 if x['Motor_Type'] == 'motorless' else x['Is_Diesel']
    df['Is_Diesel'] = df.apply(dslf, axis=1)
    df['Is_Inboard'] = df['Motor_Type'].map(lambda x: 1 if x == 'inboard' else 0)
    df.dropna(inplace=True)
    df.drop(columns=["Engine"], inplace=True)

    """=======ADJUST FOR INFLATION======"""
    df['Year_Listed'] = pd.to_datetime(df['posted_at']).dt.year
    # print(type(int(date.today().year)), int(date.today().year))
    #df['Year'] = df['Year'].astype(int)
    #df = df[(df['Year'] >= 1900)]# & (df['Year'] < int(date.today().year))]
    df = adjust_for_inflation(df)

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',
                        help='intermediates/raw_listings.csv')
    parser.add_argument('output_file',
                        help='intermediates/listings.csv')

    parser.add_argument('-dn', '--drop_null', default=True,
                        type=bool, help="Drops null values")

    args = parser.parse_args()
    print("Cleaning up listings...")
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    res = clean_transform(args.input_file, drop_null=args.drop_null)
    res.to_csv(args.output_file)
    print(f"Cleaned listings saved to {args.output_file}")
