"""
Lê os arquivos baixados de PLD e transforma ele em um formato onde cada submercado é uma coluna.

Os dados estão em dois arquivos separados, pois a CCEE fornece apenas um arquivo histórico que não está atualizado
até os dias atuais, então o restante tem que ser buscado separadamente.
"""
# %%
import pandas as pd
import numpy as np

project_dir = '/home/capaci/Documents/mba-usp/tcc/tcc-mba-cd-icmc'
external_dir = f'{project_dir}/data/external'

df_pld_historico = pd.read_html(f'{external_dir}/pld-horario.xls', decimal=',', thousands='.', parse_dates=True)[0]
df_pld_recente = pd.read_csv(f'{external_dir}/pld-horario-2021-12-03-a-2021-12-30.csv', sep=';', decimal=',', thousands='.', parse_dates=True)

df = df_pld_historico.merge(df_pld_recente, on=['Hora', 'Submercado'])
# %%
df.head()
# %%
colunas_concat = list(df.columns)

# %%
# https://stackoverflow.com/a/28654127/6071444
df = df.melt(id_vars=["Submercado", "Hora"], 
             var_name="Data", 
             value_name="Valor",
             )

df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
df['Data'] = df['Data'] +  pd.to_timedelta(df['Hora'], unit='h')
df = df.drop(columns=['Hora']).rename(columns={'Data': 'Data_Hora_Referencia'})



# %%
# por algum motivo, tinha valores duplicados
duplicated_keep_false = df[df.duplicated(subset=['Submercado', 'Data_Hora_Referencia'], keep=False)]
duplicated_default = df[df.duplicated(subset=['Submercado', 'Data_Hora_Referencia'])]
xablau = df.drop(index=duplicated_keep_false.isnull().index)


# %%
print(f'{df.shape=}\n{xablau.shape=}\n{duplicated_keep_false.shape=}\n{duplicated_default.shape=}')

# %%
xablau = xablau.pivot(index='Data_Hora_Referencia', columns='Submercado', values='Valor')
# %%
xablau = xablau.resample('H').interpolate('linear')
# %%
xablau.to_csv(f'{project_dir}/data/raw/pld-horario.csv')
# %%

