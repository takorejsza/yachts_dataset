import pickle
import pandas as pd

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('Length')
    parser.add_argument('Year')
    parser.add_argument('Beam')
    parser.add_argument('Draft')
    parser.add_argument('Cabins')
    parser.add_argument('Is_Mono')
    parser.add_argument('Is_Diesel')
    parser.add_argument('Is_Cutter')
    parser.add_argument('Is_Ketch')
    parser.add_argument('Is_masthead_sloop')
    parser.add_argument('Is_Excellent')
    parser.add_argument('Is_Fair')
    parser.add_argument('Is_Good')
    parser.add_argument('Is_project_boat')
    parser.add_argument('Engine_Count')
    parser.add_argument('Is_Inboard')
    parser.add_argument('Year_Listed')
    parser.add_argument('Is_Cruiser')
    parser.add_argument('Is_Daysailer')

    #parser.add_argument('-m', '--model',type=argparse.FileType('rb'),default='trained_model.pkl', help='trained model file(PKL)')
    parser.add_argument('model',help='data_modeling/trained_model.pkl')

    args = parser.parse_args()

    #model = pickle.load(args.model)
    with open(args.model, 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict(pd.DataFrame([{
        'Length': args.Length,
        'Year': args.Year,
        'Beam': args.Beam,
        'Draft': args.Draft,
        'Cabins': args.Cabins,
        'Is_Mono': args.Is_Mono,
        'Is_Diesel': args.Is_Diesel,
        'Is_Cutter': args.Is_Cutter,
        'Is_Ketch': args.Is_Ketch,
        'Is_masthead_sloop': args.Is_masthead_sloop,
        'Is_Excellent': args.Is_Excellent,
        'Is_Fair': args.Is_Fair,
        'Is_Good': args.Is_Good,
        'Is_project_boat': args.Is_project_boat,
        'Engine_Count': args.Engine_Count,
        'Is_Inboard': args.Is_Inboard,
        'Year_Listed': args.Year_Listed,
        'Is_Cruiser': args.Is_Cruiser,
        'Is_Daysailer': args.Is_Daysailer,
        
  
        
    }])).round(1)[0]
        
    print(f'The estimated price of the inputted Boat is --> $ {prediction}')