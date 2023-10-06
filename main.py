from bs4 import BeautifulSoup
import requests
import re
import json
import pprint
from deep_translator import GoogleTranslator
from tqdm import tqdm

pp = pprint.PrettyPrinter()
response = requests.get('https://fr.wikipedia.org/wiki/Chronologie_de_l%27exploration_spatiale')
content = response.text

soup = BeautifulSoup(content, 'html.parser')
table = soup.select_one('table.wikitable')
table_rows = table.find_all('tr')

all_data = []

for row in tqdm(table_rows):
    columns = row.find_all('td')
    if columns:
        current_data = {}

        # GET DATE:
        current_data['DATE'] = GoogleTranslator(source='fr', target='en').translate(columns[0].text.replace('\n', ''))

        # GET COUNTRIES:
        # The scrapped data is only available on the French part of Wikipedia, that's why we have to translate it
        # into English
        countries = columns[1].find_all('a')[-1].text or []
        if not countries:
            all_countries_tags = columns[1].find_all('a')
            for country in all_countries_tags:
                match = re.search(r"(?:de la|de l’|des|du)(.*)", country['title'])
                countries.append(match.group(1).strip())
        if isinstance(countries, list):
            countries = [GoogleTranslator(source='fr', target='en').translate(country.upper()) for country in countries]
        else:
            countries = GoogleTranslator(source='fr', target='en').translate(countries.upper())
        current_data['COUNTRY'] = countries

        # GET DESCRIPTION:
        current_data['DESCRIPTION'] = GoogleTranslator(source='fr', target='en').translate(columns[2].text.replace('\n', ''))

        # GET IMAGE SOURCE:
        current_data['IMAGE_LINK'] = columns[3].find('img') and columns[3].find('img')['src'] if len(columns) > 3 else \
            None

        # ADD DATA:
        all_data.append(current_data)

pp.pprint(all_data)

# EXPORT TO JSON
with open(r'C:\Users\33634\Desktop\Space-App\assets\data\historical_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_data, json_file, ensure_ascii=False, indent=4)




