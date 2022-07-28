import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

def get_info_from_every_boat(hyperlinks):
    
    main_dictionary = dict()
    i = 0
    for links in hyperlinks:
        page = urlopen(links).read()
        soup = BeautifulSoup(page,'html.parser')
        for link in soup.find_all('a',{'class':'sailheader'}):
            response = requests.get(link.get('href')).text
            meta = dict()
            if len(BeautifulSoup(response, 'html.parser').find_all('h1')) > 0:
                meta['Model'] = re.findall(r"(?<=</span> ).*(?=</h1>)", str(BeautifulSoup(response, 'html.parser').find_all('h1')[0]))[0]
                meta['posted_at'] = re.findall(r"(?<=Added ).*(?=\n\t\t\t\t\t\n</font>)",str(BeautifulSoup(response, 'html.parser').find_all('font',{'color':'#666666','face':'verdana,arial,helvetica','size':'-2'})[3]))[0]
                boat_info = BeautifulSoup(response, 'html.parser').find_all('td',{"height":"20", "width":"121"})
                info_list = [ele.text.strip('\n') for ele in boat_info]
                meta.update(dict([([ele for ele in info_list][i],[ele for ele in info_list][i+6]) for i in [0,1,2,3,4,5,12,13,14,15,16,17]]))
                main_dictionary[str(i)] = meta
            else:
                pass
            i= i+1
     
    df = pd.DataFrame.from_dict(main_dictionary, orient='index').drop_duplicates()

    return df


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='intermediates/saved_hyperlinks.txt')
    parser.add_argument('output_file',help='intermediates/additional_features_dataset.csv')
    #parser.add_argument('-v', '--verbose', action='store_true', help='display metrics')
    args = parser.parse_args()

    with open(args.input_file) as file:
        links = file.readlines()
    print('Scraping https://www.sailboatlistings.com/sailboats_for_sale/')
    df = get_info_from_every_boat(set(links))

    os.makedirs(r"./data", exist_ok=True)
    df.to_csv(args.output_file)
  