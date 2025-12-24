import os
import pandas as pd

from pathlib import Path

# pdvd и marpor джойнятся по id партии и дате голосования/выборов (предшествующие голосованию выборы)
# pdvd и ches джойнятся по id партии и дате голосования/наблюдения (предшествующие голосованию оценки)
# pdvd и dpi джойнятся по стране (надо привести к одной системе)

# в датасете pdvd_party_votes и pdvd_votes были обнаружены опечатки в датировке отдельных голосований
# эти ошибки не позволяли корректно сджойнить датасеты
# при репликации следует пользоваться файлами, расположенными в текущей директории, или самостоятельно 
# устранить ошибки 

pdvd_party_votes = [
    'country', 
    'year_vote', 
    'date_vote', 
    'mission_name',
    'Party_name_full_EN',
    'CMP_ID', 
    'party_family_PDVD',
    'regional_party', 
    'share_yes_votes', 
    'gov_opp_num',
    'withdrawal_or_anti_interventionvote',
    'document_ID_URL'
]

pdvd_votes = [
    'country',
    'membership_alliance',
    'membership_UNSC',
    'date_vote',
    'mission',
    'vote_name_native'
]

marpor = [
    'edate',
    'party',
    'rile',
    'pervote'
]

ches = [
    'year',
    'cmp_id',
    'lrgen'
]

dpi = [
    'ifs',
    'year',
    'herfgov'
]

code_map = {
    'AUL': 'AUS',  # Australia
    'BEL': 'BEL',  # Belgium
    'CAN': 'CAN',  # Canada
    'CRO': 'HRV',  # Croatia
    'CZE': 'CZE',  # Czech Republic
    'DEN': 'DNK',  # Denmark
    'FIN': 'FIN',  # Finland
    'FRN': 'FRA',  # France
    'GMY': 'DEU',  # Germany
    'IRE': 'IRL',  # Ireland
    'ITA': 'ITA',  # Italy
    'JPN': 'JPN',  # Japan
    'LIT': 'LTU',  # Lithuania
    'NTH': 'NLD',  # Netherlands
    'ROK': 'KOR',  # South Korea
    'ROM': 'ROM',  # Romania
    'SLO': 'SVN',  # Slovenia
    'SPN': 'ESP',  # Spain
    'TUR': 'TUR',  # Turkey
    'UKG': 'GBR',  # United Kingdom
    'USA': 'USA'   # United States
}

PROJECT_ROOT = Path(__file__).resolve().parents[1]

path_to_raw_data = PROJECT_ROOT.joinpath('data/raw')
path_to_processed_data = PROJECT_ROOT.joinpath('data/processed')

dataframes = {}

for item in os.listdir(path_to_raw_data):
    filename = os.path.splitext(item)[0]
        
    if item.endswith('.xlsx'):
        dataframes[filename] = pd.read_excel(os.path.join(path_to_raw_data, item))
        print(f"Добавлен DataFrame: {filename}")
    elif item.endswith('.csv'):
        dataframes[filename] = pd.read_csv(os.path.join(path_to_raw_data, item))
        print(f"Добавлен DataFrame: {filename}")

#for name, df in dataframes.items():
#    dataframes[name] = df.drop_duplicates(ignore_index=True)

columns_mapping = {
    'pdvd_party_votes': pdvd_party_votes,
    'pdvd_votes': pdvd_votes,
    'marpor': marpor,
    'ches': ches,
    'dpi': dpi
}

for name, df in dataframes.items():
    if name in columns_mapping:
        cols_to_keep = columns_mapping[name]
        existing_cols = [col for col in cols_to_keep if col in df.columns]
        dataframes[name] = df[existing_cols]
        
        print(f"Оставлены столбцы в {name}: {existing_cols}")

# приведем id партии к строковому типу
dataframes['pdvd_party_votes']['CMP_ID'] = dataframes['pdvd_party_votes']['CMP_ID'].apply(lambda x: str(x).split('.')[0])
dataframes['ches']['cmp_id'] = dataframes['ches']['cmp_id'].apply(lambda x: str(x).split('.')[0])
dataframes['marpor']['party'] = dataframes['marpor']['party'].apply(lambda x: str(x).split('.')[0])

merged = pd.merge_asof(
    dataframes['pdvd_party_votes'].sort_values(by='year_vote'),
    dataframes['ches'].sort_values(by='year'),
    left_by='CMP_ID',
    right_by='cmp_id',
    left_on='year_vote',
    right_on='year'
              )

merged = pd.merge_asof(
    merged.sort_values(by='date_vote'),
    dataframes['marpor'].sort_values(by='edate'),
    left_by='CMP_ID',
    right_by='party',
    left_on='date_vote',
    right_on='edate'
    )

# перекодируем кодировки стран
merged['country_iso3'] = merged['country'].map(code_map)
dataframes['dpi']['year'] = dataframes['dpi']['year'].dt.year

merged = pd.merge(merged, dataframes['dpi'],
         left_on=['country_iso3', 'year_vote'],
         right_on=['ifs', 'year'])

merged = pd.merge_asof(
    merged.sort_values(by='date_vote'),
    dataframes['pdvd_votes'].sort_values(by='date_vote'),
    on='date_vote',
    left_by=['country'],
    right_by=['country'],
    direction='nearest',
    tolerance=pd.Timedelta(days=10)
    )

merged['date_vote'] = merged['date_vote'].dt.date

merged = merged.drop(columns=[
    'year_x',
    'country_iso3',
    'cmp_id',
    'edate',
    'party',
    'mission',
    'vote_name_native',
    'ifs',
    'year_y'
])

merged = merged.rename(columns={
    'Party_name_full_EN':'party_name',
    'CMP_ID':'cmp_id',
    'party_family_PDVD':'party_family',
    'membership_UNSC':'membership_unsc',
    'document_ID_URL':'document_id_url'
    })

merged = merged.sort_values(by=['country', 'date_vote', 'mission_name', 'party_name'])

merged.to_excel(os.path.join(path_to_processed_data, 'votes.xlsx'), index=False)
print(f"Файл сохранен")