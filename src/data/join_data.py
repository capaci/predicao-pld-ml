# %%
import pandas as pd
import numpy as np
import os

current_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))

external_dir = f'{project_dir}/data/external'
arq_pld = f'{project_dir}/data/raw/pld-horario.csv'
arq_carga_energia = f'{external_dir}/ons/carga-energia.csv'
arq_ear = f'{external_dir}/ons/ear.csv'
arq_ena = f'{external_dir}/ons/ena.csv'
arq_geracao = f'{external_dir}/ons/geracao-gwh.csv'
arq_demanda = f'{project_dir}/data/external/ons/demanda-maxima-mwh.csv'
arq_cmo = f'{project_dir}/data/external/ons/cmo-semi-horario.xlsx'
arq_intercambio = f'{external_dir}/ons/intercambio-nacional.csv'

pld = pd.read_csv(arq_pld, index_col='Data_Hora_Referencia', parse_dates=True)
carga_energia = pd.read_csv(arq_carga_energia, parse_dates=True)
ear = pd.read_csv(arq_ear, parse_dates=True)
ena = pd.read_csv(arq_ena, parse_dates=True)
geracao = pd.read_csv(arq_geracao, sep=';', decimal=',', thousands='.')
demanda = pd.read_csv(arq_demanda, sep=';', decimal=',', thousands='.')
cmo = pd.read_excel(arq_cmo,
                    sheet_name=None,
                    thousands='.',
                    index_col='Data',
                    parse_dates=True,
                    )

intercambio = pd.read_csv(arq_intercambio, parse_dates=True)

# %%
def reshape_pld_df(df):
    return (
        df
        .resample('D')
        .mean()
        .round(2)
        .melt(value_vars=['NORDESTE', 'NORTE', 'SUDESTE', 'SUL'],
              var_name='subsistema',
              value_name='pld_medio',
              ignore_index=False,
              )
        .reset_index()
        .rename(columns={'Data_Hora_Referencia': 'data'})
    )

# %%


def agrupa_intercambio_por_dia(df):
    df['din_instante'] = pd.to_datetime(df['din_instante'])
    return (
        df
        .drop(columns=['id_subsistema_origem', 'id_subsistema_destino', 'nom_subsistema_destino'])
        .groupby([pd.Grouper(key='din_instante', freq='D'), 'nom_subsistema_origem'])
        .sum()
        .reset_index()
    )


# %%
def trata_dados_demanda(demanda):
    df = pd.DataFrame()
    df['data'] = pd.to_datetime(
        demanda['Data Escala de Tempo 1 DM Comp 3'], format='%d/%m/%Y %H:%M:%S')
    df['subsistema'] = (
        demanda['Subsistema']
        .str.upper()
        .str.replace('SUDESTE/CENTRO-OESTE', 'SUDESTE', regex=False)

    )
    df['demanda_mwh'] = demanda['Selecione Tipo de DM Comp 3 (copy)']

    return df

# %%


def trata_geracao(geracao):
    df = pd.DataFrame()
    df['data'] = pd.to_datetime(
        geracao['Data Escala de Tempo 1 GE Comp 3'], format='%d/%m/%Y %H:%M:%S')
    df['subsistema'] = (
        geracao['Selecione Comparar GE Comp 3']
        .str.upper()
        .str.replace('SUDESTE/CENTRO-OESTE', 'SUDESTE', regex=False)
    )
    df['geracao_gwh'] = geracao['Selecione Tipo de GE Comp 3']
    df = df.dropna()
    return df


# %%
def concatenate_cmo_in_single_df(cmo: dict) -> pd.DataFrame:
    _cmo = {}
    for subsistema, df in cmo.items():
        _df = df.replace(',', '.', regex=True).astype(float)
        _cmo[subsistema.upper()] = _df.mean(axis=1).round(2)

    _cmo = (
        pd.DataFrame(_cmo)
        .resample('D')
        .interpolate()
        .reset_index()
        .rename(columns={'Data': 'data', 'SUDESTE - CENTRO-OESTE': 'SUDESTE'})
        .melt(id_vars='data', var_name='subsistema', value_name='cmo_blr_mwh')
    )
    return _cmo


# %%
def filtra_df_por_data(df, dt_col, data_inicio, data_fim):
    return df.loc[(df[dt_col] >= data_inicio) & (df[dt_col] <= data_fim)].copy()


# %%
pld_media_diaria = reshape_pld_df(pld)
# %%
intercambio_diario = agrupa_intercambio_por_dia(intercambio)

# %%
_demanda = trata_dados_demanda(demanda)
# %%
_geracao = trata_geracao(geracao)

# %%
_cmo = concatenate_cmo_in_single_df(cmo)

# %%
print(f'{carga_energia.shape=}')
print(f'{ear.shape=}')
print(f'{ena.shape=}')
print(f'{pld_media_diaria.shape=}')
print(f'{_demanda.shape=}')
print(f'{_geracao.shape=}')
print(f'{_cmo.shape=}')
print(f'{intercambio_diario.shape=}')

# %%
dt_min = pld_media_diaria['data'].min().strftime('%Y-%m-%d')
dt_max = pld_media_diaria['data'].max().strftime('%Y-%m-%d')
_carga_energia = filtra_df_por_data(
    carga_energia, 'din_instante', dt_min, dt_max)
_intercambio_diario = filtra_df_por_data(
    intercambio_diario, 'din_instante', dt_min, dt_max)
_ear = filtra_df_por_data(ear, 'ear_data', dt_min, dt_max)
_ena = filtra_df_por_data(ena, 'ena_data', dt_min, dt_max)
_demanda = filtra_df_por_data(_demanda, 'data', dt_min, dt_max)
_geracao = filtra_df_por_data(_geracao, 'data', dt_min, dt_max)
_cmo = filtra_df_por_data(_cmo, 'data', dt_min, dt_max)

# %%
print(f'{_carga_energia.shape=}')
print(f'{_intercambio_diario.shape=}')
print(f'{_ear.shape=}')
print(f'{_ena.shape=}')
print(f'{_demanda.shape=}')
print(f'{_geracao.shape=}')
print(f'{_cmo.shape=}')
print(f'{pld_media_diaria.shape=}')

# %%
left_on = ['data', 'subsistema']
_ear['ear_data'] = pd.to_datetime(_ear['ear_data'])
_ena['ena_data'] = pd.to_datetime(_ena['ena_data'])
_carga_energia['din_instante'] = pd.to_datetime(_carga_energia['din_instante'])
_cmo['data'] = pd.to_datetime(_cmo['data'])
_intercambio_diario['din_instante'] = pd.to_datetime(
    _intercambio_diario['din_instante'])

resultado = (
    pld_media_diaria
    .merge(_ear, left_on=left_on, right_on=['ear_data', 'nom_subsistema'])
    .merge(_ena, left_on=left_on, right_on=['ena_data', 'nom_subsistema'])
    .merge(_carga_energia, left_on=left_on, right_on=['din_instante', 'nom_subsistema'])
    .merge(_demanda, left_on=left_on, right_on=left_on)
    .merge(_geracao, left_on=left_on, right_on=left_on)
    .merge(_cmo, left_on=left_on, right_on=left_on)
    # .merge(_intercambio_diario, left_on=left_on, right_on=['din_instante', 'nom_subsistema_origem'], how='outer')
    .fillna(0)
)
# %%
resultado.columns
# %%
resultado = resultado.drop(columns=['id_subsistema_x',
                                    'nom_subsistema_x',
                                    'ear_data',
                                    'id_subsistema_y',
                                    'nom_subsistema_y',
                                    'ena_data',
                                    'id_subsistema',
                                    'nom_subsistema',
                                    'din_instante',
                                    ])


# %%
resultado.head()

# %%
resultado.columns

# %%
columns_to_rename = {
    'ear_max_subsistema': 'ear_max',
    'ear_verif_subsistema_mwmes': 'ear_verif_mwmes',
    'ear_verif_subsistema_percentual': 'ear_verif_percentual',
    'ena_bruta_regiao_mwmed': 'ena_bruta_mwmed',
    'ena_bruta_regiao_percentualmlt': 'ena_bruta_percentual',
    'ena_armazenavel_regiao_mwmed': 'ena_armazenavel_mwmed',
    'ena_armazenavel_regiao_percentualmlt': 'ena_armazenavel_percentual',
    'val_cargaenergiamwmed': 'carga_mwmed',
}
resultado = resultado.rename(columns=columns_to_rename)
# %%
resultado.head()
# %%
resultado.to_csv(f'{project_dir}/data/raw/dados.csv', index=False)

# %%
