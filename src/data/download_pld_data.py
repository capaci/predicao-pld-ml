# %%
import locale
import logging
import os
from datetime import date
from typing import Literal
from urllib.parse import urlencode

import pandas as pd


logger = logging.getLogger(__name__)


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

current_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
default_filepath = f'{project_dir}/data/external/pld-mensal.csv'

PriceTypes = Literal['HORARIO', 'SEMANAL', 'MENSAL']


def download_pld_data(init_date: date = date(2001, 1, 1),
                      end_date: date = date(2021, 12, 26),
                      price_type: PriceTypes = 'MENSAL',
                      output_file=default_filepath,
                      ):
    logger.info(f'Downloading PLD data from {init_date} to {end_date}')
    url = _generate_pld_url(price_type, init_date, end_date)
    df = pd.read_csv(url, sep=';', decimal=',',
                     thousands='.', parse_dates=True)
    df = df.rename(columns=str.lower)
    df['mes'] = pd.to_datetime(df['mes'], format='%b/%y')

    df.to_csv(output_file, index=False)


def _generate_pld_url(price_type: str, init_date: date, end_date: date) -> str:
    domain = 'https://www.ccee.org.br'
    path = 'web/guest/precos/painel-precos'
    vars = {
        'p_p_id': 'br_org_ccee_pld_historico_PLDHistoricoPortlet_INSTANCE_lzsn',
        'p_p_lifecycle': '2',
        'p_p_state': 'normal',
        'p_p_mode': 'view',
        'p_p_cacheability': 'cacheLevelPage',
        '_br_org_ccee_pld_historico_PLDHistoricoPortlet_INSTANCE_lzsn_inputInitialDate': init_date.strftime('%d/%m/%Y'),
        '_br_org_ccee_pld_historico_PLDHistoricoPortlet_INSTANCE_lzsn_inputFinalDate': end_date.strftime('%d/%m/%Y'),
        '_br_org_ccee_pld_historico_PLDHistoricoPortlet_INSTANCE_lzsn_tipoPreco': price_type,
    }
    url = f'{domain}/{path}?{urlencode(vars)}'
    return url


if __name__ == '__main__':
    filepath = f'{project_dir}/data/external/pld-horario.csv'
    download_pld_data(price_type='HORARIO',
                      init_date=date(2018, 4, 17),
                      end_date=date(2021,12, 2),
                      output_file=filepath
                      )
