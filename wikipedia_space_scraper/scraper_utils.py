import inspect
import re
import json
import os
import boto3
import logging

from deep_translator import GoogleTranslator
from .config import CONFIG, LocalConfig, LambdaConfig


def get_context_name():
    package_name = __package__
    if package_name:
        return package_name
    else:
        return inspect.currentframe().f_back.f_code.co_name


def load_existing_data():

    if isinstance(CONFIG, LocalConfig):
        logging.info(f'[LOCAL ENV] -> Trying to load data from: {CONFIG.DATA_EXPORT_PATH}')
        if os.path.exists(CONFIG.DATA_EXPORT_PATH):
            with open(CONFIG.DATA_EXPORT_PATH) as f:
                existing_data = json.load(f)
                last_date = existing_data[-1]['DATE']

            logging.info(f'[+] Previous data file found. Last date in the file: {last_date}')
            return existing_data

        logging.warning(f'[+] No data file found at: {CONFIG.DATA_EXPORT_PATH}')
        return False

    elif isinstance(CONFIG, LambdaConfig):
        logging.info(
            f'[AWS ENV] -> Attempting to load data file from Bucket: {CONFIG.BUCKET_NAME}, Key: {CONFIG.DATA_EXPORT_PATH}')
        s3 = boto3.client('s3')
        try:
            response = s3.get_object(Bucket=CONFIG.BUCKET_NAME, Key=CONFIG.DATA_EXPORT_PATH)
            logging.info('[+] Data file successfully loaded from S3.')
            return json.load(response["Body"])
        except s3.exceptions.NoSuchKey:
            logging.warning(f'[+] No data file found in S3 at Key: {CONFIG.DATA_EXPORT_PATH}')
            return False

    raise RuntimeError(
        f"Invalid CONFIG detected. CONFIG must be an instance of either LocalConfig or LambdaConfig. "
        f"Current CONFIG: {type(CONFIG).__name__}"
    )


def export_data_to_s3(updated_data):
    try:
        logging.info(f'[+] Uploading updated data file to bucket {CONFIG.BUCKET_NAME}..')
        s3 = boto3.client('s3')
        s3.put_object(Bucket=CONFIG.BUCKET_NAME, Key=CONFIG.DATA_EXPORT_PATH, Body=json.dumps(updated_data))
        logging.info(f'[+] DONE!')
    except Exception as e:
        logging.warning(f'[!] Error uploading file to S3: {e}')


def export_data_to_json(updated_data):
    try:
        logging.info(f'[+] Uploading updated data file to {CONFIG.DATA_EXPORT_PATH}..')
        with open(CONFIG.DATA_EXPORT_PATH, 'w', encoding='utf-8') as json_file:
            json.dump(updated_data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.warning(f'[!] Error uploading file: {e}')


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

    def export_data(data):

        if isinstance(CONFIG, LocalConfig):
            export_data_to_json(data)

        elif isinstance(CONFIG, LambdaConfig):
            export_data_to_s3(data)

    return {'scrap_data': scrap_data, 'export_data': export_data}
