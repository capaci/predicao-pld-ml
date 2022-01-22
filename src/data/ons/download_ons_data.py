import logging
import os
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from dotenv import find_dotenv, load_dotenv


# EAR_URL = 'https://ons-dl-prod-opendata.s3.amazonaws.com/dataset/ear_subsistema_di/EAR_DIARIO_SUBSISTEMA_{year}.csv'
BASE_URL = 'https://ons-dl-prod-opendata.s3.amazonaws.com/dataset/'
logger = logging.getLogger(__name__)


all_data = [
    {
        'name': 'EAR - Energia Armazenada',
        'base_url': urljoin(BASE_URL, 'ear_subsistema_di/EAR_DIARIO_SUBSISTEMA_{year}.csv'),
        'output_file': 'ear',
        'range_years': range(2018, 2022),
        'dictionary_url': urljoin(BASE_URL, 'ear_subsistema_di/DicionarioDados_EarPorSubsistema.pdf'),
    },
    {
        'name': 'Intercambio nacional',
        'base_url': urljoin(BASE_URL, 'intercambio_nacional_ho/INTERCAMBIO_NACIONAL_{year}.csv'),
        'output_file': 'intercambio-nacional',
        'range_years': range(2018, 2022),
        'dictionary_url': urljoin(BASE_URL, 'intercambio_nacional_ho/DicionarioDados_Intercambio_Nacional.pdf'),
    },
    {
        'name': 'Carga Energia',
        'base_url': urljoin(BASE_URL, 'carga_energia_di/CARGA_ENERGIA_{year}.csv'),
        'output_file': 'carga-energia',
        'range_years': range(2018, 2022),
        'dictionary_url': urljoin(BASE_URL, 'carga_energia_di/DicionarioDados_Carga_Energia.pdf'),
    },
    {
        'name': 'ENA - Energia Natural Afluente',
        'base_url': urljoin(BASE_URL, 'ena_subsistema_di/ENA_DIARIO_SUBSISTEMA_{year}.csv'),
        'output_file': 'ena',
        'range_years': range(2018, 2022),
        'dictionary_url': urljoin(BASE_URL, 'ena_subsistema_di/DicionarioDados_EnaPorSubsistema.pdf'),
    },
]


def get_data_and_concat_to_single_csv(base_url, output_file='ear.csv', range_years=range(2019, 2020)):
    content = [
        _get_single_year_data(base_url.format(year=year))
        for year in range_years
    ]
    pd.concat(content).to_csv(output_file, index=False)


def _get_single_year_data(url):
    logger.info(f'Downloading {url}')
    return pd.read_csv(url, sep=';')


def download_data_dictionary(output_file, dictionary_url):
    logger.info(f'Downloading {dictionary_url}')
    result = requests.get(dictionary_url)
    file = Path(output_file)
    file.write_bytes(result.content)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[3]

    output_dir = os.path.join(project_dir, 'data/external/ons')
    os.makedirs(output_dir, exist_ok=True)


    dictionaries_dir = os.path.join(output_dir, 'dictionaries')
    os.makedirs(dictionaries_dir, exist_ok=True)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    for data in all_data:
        logger.info(f'Downloading {data["name"]}')
        get_data_and_concat_to_single_csv(
            data['base_url'],
            os.path.join(output_dir, f'{data["output_file"]}.csv'),
            data['range_years']
        )

        if data['dictionary_url']:
            download_data_dictionary(
                os.path.join(dictionaries_dir, f'{data["output_file"]}.pdf'),
                data['dictionary_url']
            )

