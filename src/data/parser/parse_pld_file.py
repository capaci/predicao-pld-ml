# %%
import pandas as pd

def parse(filepath: str) -> pd.DataFrame:
    return (
        _read_file(filepath)
        .pipe(_rename_columns_to_lower)
        .pipe(_transform_date_to_month_period)
    )


def _read_file(filepath: str) -> pd.DataFrame:
    df = pd.read_html(filepath, thousands='.', decimal=',', parse_dates=True, index_col='MES')
    return df[0]


def _transform_date_to_month_period(df: pd.DataFrame) -> pd.DataFrame:
    df['mes'] = df.index.to_period('M')
    df = df.set_index('mes')
    return df


def _rename_columns_to_lower(df:pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=str.lower)


if __name__ == '__main__':
    project_dir = '/home/capaci/Documents/mba-usp/tcc/tcc-mba-cd-icmc'
    filepath = f'{project_dir}/data/external/Histórico do Preço Médio Mensal janeiro de 2001 a novembro de 2021.xls'

    df = parse(filepath)
    df.to_csv(f'{project_dir}/data/external/pld.csv')
    print(df)
