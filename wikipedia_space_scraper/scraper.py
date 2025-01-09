import logging
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from tqdm import tqdm

from .scraper_utils import get_context_name, scraper_closure, load_existing_data
from .config import CONFIG

SCRIPT_NAME = get_context_name()
logging.basicConfig(level=logging.INFO)


def scrape_wikipedia_data():

    response = requests.get(CONFIG.WIKIPEDIA_URL)
    content = response.text

    soup = BeautifulSoup(content, 'html.parser')
    table = soup.select_one('table.wikitable')
    table_rows = table.find_all('tr')

    new_data = []
    existing_data = load_existing_data()

    if existing_data:

        last_date = existing_data[-1]['DATE']
        existing_data_handler = scraper_closure()
        scrap_data = existing_data_handler['scrap_data']
        export_data = existing_data_handler['export_data']

        for row in tqdm(reversed(table_rows)):
            columns = row.find_all('td')
            if columns:
                scraped_date = GoogleTranslator(source='fr', target='en').translate(columns[0].text.replace('\n', ''))

                # Check if all the data has been scraped
                if scraped_date == last_date:
                    logging.info(f'{SCRIPT_NAME} - {CONFIG.DATA_EXPORT_FILENAME} is up to date!')
                    break

                # Scrap new data:
                logging.info(f'{SCRIPT_NAME} - New data found for {scraped_date} (added to {CONFIG.DATA_EXPORT_PATH})')
                new_data.append(scrap_data(columns, date=scraped_date))
        if new_data:
            existing_data.extend(reversed(new_data))
            export_data(data=existing_data)

    # Else scrap data from beginning:
    else:
        new_data_handler = scraper_closure()
        scrap_data = new_data_handler['scrap_data']
        export_data = new_data_handler['export_data']
        for row in tqdm(table_rows):
            columns = row.find_all('td')
            if columns:
                new_data.append(scrap_data(columns))
        else:
            export_data(data=new_data)

    return f'[+] {SCRIPT_NAME} - Done'
