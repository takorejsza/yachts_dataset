import os
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from tqdm import tqdm

def get_listings(links:set):
    print(f"number of webpages: {len(links)}")
    dataframes = list()
    for link in tqdm(links):
        response = requests.get(link).text
        soup = BeautifulSoup(response, 'html.parser').find_all("td")
        counter = 0
        main_dictionary = dict()
        for j, x in enumerate(soup):
            meta = dict()
            boats = x.find_all('span')
            for i, o in enumerate(boats):
                if o.get('class')[0] == 'sailheader':
                    meta['Model'] = o.text
                if o.get('class')[0] == 'sailvb':
                    feature = o.text
                if o.get('class')[0] == 'sailvk':
                    meta[feature] = o.text
                if o.get('class')[0] == 'details':
                    regex = re.compile(r"[0-9]+-[A-Z][a-z]+-[0-9]+")
                    meta['posted_at'] = re.findall(regex, o.text)[0]

            if ('Model' not in meta.keys()) | ('Asking: ' not in meta.keys()):
                continue

            main_dictionary[str(j)] = meta

        result = pd.DataFrame.from_dict(main_dictionary, orient='index')\
                .drop_duplicates()

        dataframes.append(result)

    return pd.concat(dataframes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='intermediates/saved_hyperlinks.txt')
    parser.add_argument('output_file', help='intermediates/raw_listings.csv')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    with open(args.input_file) as file:
        links = file.readlines()
    print('Scraping https://www.sailboatlistings.com/sailboats_for_sale/')
    df = get_listings(set(links))
    df.to_csv(args.output_file)
