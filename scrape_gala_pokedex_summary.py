import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

g2e = {
    'normal': 'Normal',
    "kampf": 'Fight',
    "flug": 'Flying',
    "gift": 'Poison',
    "boden": 'Ground',
    "gestein": 'Rock',
    "kaefer": 'Bug',
    "geist": 'Ghost',
    "stahl": 'Steel',
    "feuer": 'Fire',
    "wasser": 'Water',
    "pflanze": 'Grass',
    "elektro": 'Electric',
    "psycho": 'Psychic',
    "eis": 'Ice',
    "drache": 'Dragon',
    "unlicht": 'Dark',
    "fee": 'Fairy',
}

def scrape_pokewiki_table(url):
    res = pd.DataFrame()

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find('table').find('tbody').find_all('tr')

    for row in tqdm(rows):
        cells = row.find_all('td')

        ser = pd.Series()
        ser['id'] = int(cells[0].text)
        ser['name'] = cells[1].text.strip()

        imgs = cells[2].find_all('img')
        t0 = g2e[imgs[0].get('alt').lower()]
        if len(imgs) == 2:
            t1 = g2e[imgs[1].get('alt').lower()]
            ser['type1'] = min(t0, t1)
            ser['type2'] = max(t0, t1)
        else:
            ser['type1'] = t0
        ser['n_type'] = len(imgs)
        res = res.append(ser, ignore_index=True)

    return res


if __name__ == '__main__':
    pokewiki_url = 'https://www.bisafans.de/spiele/editionen/schild-schwert/galar-dex.php'

    df = scrape_pokewiki_table(pokewiki_url)

    print(df.head())

    df.to_csv('./pokedex_summary.csv')

