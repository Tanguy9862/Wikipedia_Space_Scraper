from deep_translator import GoogleTranslator
import re
import json


def scraper_closure():

    def scrap_data(columns, date=None):
        # GET DATE:
        current_data = {
            'DATE': date or GoogleTranslator(source='fr', target='en').translate(columns[0].text.replace('\n', ''))
        }

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
        current_data['DESCRIPTION'] = GoogleTranslator(source='fr', target='en').translate(
            columns[2].text.replace('\n', ''))

        # GET IMAGE SOURCE:
        current_data['IMAGE_LINK'] = columns[3].find('img') and columns[3].find('img')['src'] if len(columns) > 3 else \
            None

        return current_data

    def export_to_json(path, data):
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    return {'scrap_data': scrap_data, 'export_to_json': export_to_json}

