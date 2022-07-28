import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_save(data, variables, response, seed=42):

    X = data[variables[:-1]]
    y = data[[response]]

    data = train_test_split(X, y, shuffle=True, random_state=seed)

    files = ['X_train', 'X_test', 'y_train', 'y_test']
    
    if not os.path.isdir(r"data/"):
        os.mkdir("data")
    
    for f, d in zip(files, data):
        d.to_csv(f"data/{f}.csv", index=False)

if __name__ == "__main__":
    import argparse
    
    FEATURES = [
        'Length','Year','Beam','Draft','Is_Mono','Is_Diesel','Engine_Count','Cabins','Is_Inboard','Year_Listed','Is_Fiberglass',
        'Is_cruiser','Is_daysailer','Is_masthead_sloop','Is_Cutter','Is_Ketch','Is_Excellent','Is_Fair','Is_Good','Is_Project_boat']
    parser = argparse.ArgumentParser()

    parser.add_argument('f', type=str, help='raw csv file with headers')
    parser.add_argument('r', type=str, help='response')
    parser.add_argument(
        '-v', type=str, nargs='*', default=FEATURES,
        help='variables'
    )

    args = parser.parse_args()
    columns = args.v
    columns.append(args.r)

    df = pd.read_csv(args.f)[columns]
    
    split_save(df, args.v, args.r)

