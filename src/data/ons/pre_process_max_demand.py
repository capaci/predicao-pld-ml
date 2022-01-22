import os

import pandas as pd


def pre_process_max_demand(input_file: str, output_file: str):
    df = (
        _read_file(input_file)
        .pipe(_add_subsystem_id_column)
        .pipe(_drop_useless_columns)
        .pipe(_rename_columns)
        .pipe(_convert_date_string_to_datetime)
    )
    df.to_csv(output_file, index=False)
    return df

def _convert_date_string_to_datetime(df):
    df['data'] = pd.to_datetime(df['data'])
    return df


def _read_file(input_file):
    df = pd.read_csv(
        input_file,
        parse_dates=True,
        decimal=',',
        thousands='.',
        sep=';'
    )

    return df


def _add_subsystem_id_column(df: pd.DataFrame) -> pd.DataFrame:
    subsystem_replace = {
        'Sul': 'S',
        'Sudeste/Centro-Oeste': 'SE',
        'Norte': 'N',
        'Nordeste': 'NE',
    }

    df['id_subsistema'] = df['Subsistema'].replace(subsystem_replace)
    return df


def _drop_useless_columns(df):
    columns_to_drop = [
        'Din Instante',
        'Data Escala de Tempo 1 DM Comp 3.1',
        'Data do Incio da Semana Din Instante DM Comp 3',
        'Texto Data Incio da Semana Din Instante DM',
        'Período Exibido DM Comp 3',
    ]
    df = df.drop(columns=columns_to_drop)
    return df


def _rename_columns(df):
    columns_to_rename = {
        'Data Escala de Tempo 1 DM Comp 3': 'data',
        'Subsistema': 'subsistema',
        'Selecione Tipo de DM Comp 3 (copy)': 'demanda_maxima',
    }
    df = df.rename(columns=columns_to_rename)
    return df


if __name__ == '__main__':
    output_dir = '/home/capaci/Documents/mba-usp/tcc/tcc-mba-cd-icmc/data/interim/ons'
    os.makedirs(output_dir, exist_ok=True)

    input_file = '/home/capaci/Documents/mba-usp/tcc/tcc-mba-cd-icmc/data/external/ons/demanda-maxima-diaria-sudeste-2001-2021.csv'
    output_file = f'{output_dir}/demanda-maxima-diaria-sudeste-2001-2021.csv'
    pre_process_max_demand(input_file=input_file, output_file=output_file)
