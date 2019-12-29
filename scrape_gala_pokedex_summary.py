import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

g2e = {
    'Normal': 'Normal',
    "Kampf": 'Fight',
    "Flug": 'Flying',
    "Gift": 'Poison',
    "Boden": 'Ground',
    "Gestein": 'Rock',
    "Käfer": 'Bug',
    "Geist": 'Ghost',
    "Stahl": 'Steel',
    "Feuer": 'Fire',
    "Wasser": 'Water',
    "Pflanze": 'Grass',
    "Elektro": 'Electric',
    "Psycho": 'Psychic',
    "Eis": 'Ice',
    "Drache": 'Dragon',
    "Unlicht": 'Dark',
    "Fee": 'Fairy',
}

def scrape_pokewiki_table(url):
    res = pd.DataFrame()

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find('table').find('tbody').find_all('tr')

    for row in tqdm(rows):
        cells = row.find_all('td')
        if len(cells) == 0:
            continue

        ser = pd.Series()
        ser['id'] = int(cells[0].text)
        ser['name'] = cells[2].text

        ser['type'] = [g2e[l.get('title')] for l in cells[3].find_all('a')]
        ser['n_type'] = len(ser['type'])
        res = res.append(ser, ignore_index=True)

    return res


if __name__ == '__main__':
    pokewiki_url = 'https://www.pokewiki.de/Liste_der_Pok%C3%A9mon_nach_Galar-Pok%C3%A9dex'

    df = scrape_pokewiki_table(pokewiki_url)

    print(df.head())

    df.to_csv('./pokedex_summary.csv')

