from bs4 import BeautifulSoup
import requests
import json
import pprint
import os
from deep_translator import GoogleTranslator
from tqdm import tqdm
from scraper_utils import scraper_closure

PATH_TO_EXPORT = 'data'
DATA_FILENAME = 'historical_data.json'
SCRIPT_NAME = os.path.basename(os.getcwd())

pp = pprint.PrettyPrinter()
response = requests.get('https://fr.wikipedia.org/wiki/Chronologie_de_l%27exploration_spatiale')
content = response.text

soup = BeautifulSoup(content, 'html.parser')
table = soup.select_one('table.wikitable')
table_rows = table.find_all('tr')

new_data = []

# If previous data exists, then scrap new data from end of the table:
has_previous_data = os.path.exists(fr'{PATH_TO_EXPORT}/{DATA_FILENAME}')
if has_previous_data:
    with open(fr'{PATH_TO_EXPORT}/{DATA_FILENAME}') as f:
        existing_data = json.load(f)
        last_date = existing_data[-1]['DATE']

    existing_data_handler = scraper_closure()
    scrap_data = existing_data_handler['scrap_data']
    export_to_json = existing_data_handler['export_to_json']

    for row in tqdm(reversed(table_rows)):
        columns = row.find_all('td')
        if columns:
            scraped_date = GoogleTranslator(source='fr', target='en').translate(columns[0].text.replace('\n', ''))
            if scraped_date == last_date:
                print(f'[+] {SCRIPT_NAME} - Historical Data is now up to date!')
                break

            # Scrap new data:
            print(f'[+] {SCRIPT_NAME} - New data found! Adding it to previous Historical Data..({scraped_date})')
            new_data.append(scrap_data(columns, date=scraped_date))
    existing_data.extend(reversed(new_data))

    # Export to JSON:
    export_to_json(path=fr'{PATH_TO_EXPORT}/{DATA_FILENAME}', data=existing_data)

# Else scrap data from beginning:
else:
    print(f'[+] {SCRIPT_NAME} - No previous data found, scraping data from zero..')
    new_data_handler = scraper_closure()
    scrap_data = new_data_handler['scrap_data']
    export_to_json = new_data_handler['export_to_json']
    for row in tqdm(table_rows):
        columns = row.find_all('td')
        if columns:
            new_data.append(scrap_data(columns))
    else:
        export_to_json(path=fr'{PATH_TO_EXPORT}/{DATA_FILENAME}', data=new_data)
