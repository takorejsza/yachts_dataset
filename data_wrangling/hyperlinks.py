import os
import argparse
import requests
from bs4 import BeautifulSoup
# Author: Thomas Korejsza
# April 6th 2022
# Update: july 5th 2022

def hyperlinks():
    homepage = r"https://www.sailboatlistings.com/sailboats_for_sale/"
    def get_pages(url=homepage):
        response = requests.get(url).text
        dom = BeautifulSoup(response, 'html.parser').find_all("div")
        links = [url]
        for x in dom:
            for o in x.find_all('div'):
                if o.get('class')[0]=="pgnum":
                    for tag in o.find_all('a'):
                        links.append(
                                     "https://www.sailboatlistings.com/" +
                                     tag.get('href')
                                     )
        return links

    hyperlinks = get_pages()
    pages = set()
    while len(hyperlinks) >= 1:
        url = hyperlinks.pop(0)
        pages.add(url)
        if len(hyperlinks) == 0:
            hyperlinks = get_pages(url=url)
            if set(hyperlinks).issubset(pages):
                break

    func = lambda page: 0 if page == homepage else int(page.split('=')[-1])
    return sorted(pages, key=func)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('of', help="location to save hyperlinks.")
    args = parser.parse_args()

    if not os.path.isdir(r"data_wrangling/intermediates/"):
        os.mkdir("data_wrangling/intermediates")
    
    path = f"data_wrangling/intermediates/{args.of}"
    with open(path, 'w') as file:
        print("Writing hyperlinks to file.")
        for page in hyperlinks():
            file.write(page+'\n')
    print(f"hyperlinks saved to {args.of}")
