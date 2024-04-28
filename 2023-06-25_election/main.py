import os
from analysis_utils import compute_all_bias, remove_defunct_parties, compute_regression, debias
import pandas as pd
from main_m import get_current_predictions
from datetime import date

# Get macro predictions
current_dir = os.getcwd()
os.chdir('/Users/pkonstan/PycharmProjects/macroeconomic_data_api')
macro_df = get_current_predictions(country='greece')
os.chdir(current_dir)


df = pd.read_csv('new_polls.csv')
df = remove_defunct_parties(df)
bias_matrix = compute_all_bias(df.copy())
bias_matrix_commissioner = compute_all_bias(df.copy(), agent='Commissioner')
debiased_df = debias(df.copy(), bias_matrix)
df_reg = compute_regression(debiased_df, start_date='2023-05-21', end_date='2023-06-25')

# Some small modifications
df_reg['Date'] = pd.to_datetime(df_reg['Date']).dt.date
df['Date'] = pd.to_datetime(df['Date']).dt.date

# Compute deviation from macro prediction
today = date.today()

drop_list = []
for i in range(len(macro_df)):

    try:
        tmp = df_reg.loc[df_reg['Date'] < today][[
            "Movement for Change_mean",
            "New Democracy_mean",
            "Communist Party of Greece_mean",
            "Coalition of the Left_mean",
            "Greek Solution_mean",
            "European Realistic Disobedience Front_mean",
            "Niki_mean",
            "Course of Freedom_mean",
            "Spartans_mean"
        ]].sort_values(by=0, axis=1, ascending=False)

        macro_df.at[i, 'vote_share'] -= tmp.iloc[-1][tmp.columns[i]]
    except:
        drop_list.append(i)

macro_df = macro_df.drop(drop_list)
macro_df = macro_df.drop(['party_id', 'election_date'], axis=1)
macro_df['vote_share'] = -macro_df['vote_share']
macro_df = macro_df.set_index('party_name_english')
macro_df = macro_df.transpose()
macro_df = macro_df.rename(columns={
    "Panhellenic Socialist Movement": "KINAL",
    "New Democracy": "ND",
    "Communist Party of Greece": "KKE",
    "Coalition of the Radical Left": "SYRIZA",
    "Greek Solution": "EL",
    "European Realistic Disobedience Front": "MERA",
    "Course of Freedom": "CF",
    "Niki": "NIKI",
    "Spartans": "SP",
                   })

macro_df.to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023-06-25_election/macro_df.csv', index=False)

# change names
df_reg = df_reg.rename(columns={
    "Movement for Change_mean": "mean_KINAL",
    "Movement for Change_std": "stdv_KINAL",
    "New Democracy_mean": "mean_ND",
    "New Democracy_std": "stdv_ND",
    "Communist Party of Greece_mean": "mean_KKE",
    "Communist Party of Greece_std": "stdv_KKE",
    "Coalition of the Left_mean": "mean_SYRIZA",
    "Coalition of the Left_std": "stdv_SYRIZA",
    "Greek Solution_mean": "mean_EL",
    "Greek Solution_std": "stdv_EL",
    "European Realistic Disobedience Front_mean": "mean_MERA",
    "European Realistic Disobedience Front_std": "stdv_MERA",
    "Niki_mean": "mean_NIKI",
    "Niki_std": "stdv_NIKI",
    "Course of Freedom_mean": "mean_CF",
    "Course of Freedom_std": "stdv_CF",
    "Spartans_mean": "mean_SP",
    "Spartans_std": "stdv_SP",
    "Date": "date",
                   })

df = df.rename(columns={
    "Movement for Change": "KINAL",
    "New Democracy": "ND",
    "Communist Party of Greece": "KKE",
    "Coalition of the Left": "SYRIZA",
    "Greek Solution": "EL",
    "European Realistic Disobedience Front": "MERA",
    "Course of Freedom": "CF",
    "Niki": "NIKI",
    "Spartans": "SP",
    "Date": "Fieldwork_date",
    "Polling Firm": "PollingFirm",
    "Sample Size": "Sample_size"
                   })

infered_polling = df_reg[[
"date",
"mean_ND",
"stdv_ND",
"mean_SYRIZA",
"stdv_SYRIZA"
]]

infered_polling_small_parties = df_reg[[
"date",
"mean_KINAL",
"stdv_KINAL",
"mean_KKE",
"stdv_KKE",
"mean_EL",
"stdv_EL",
"mean_MERA",
"stdv_MERA",
"mean_CF",
"stdv_CF",
"mean_NIKI",
"stdv_NIKI",
"mean_SP",
"stdv_SP",
]]

df[['Fieldwork date_Original']] = df[['Fieldwork_date']]
df[['Noise_level']] = 1

df = df.drop('Others', axis='columns')
df = df[['Fieldwork_date',
         'Sample_size',
         'ND',
         'SYRIZA',
         'KINAL',
         'KKE',
         'EL',
         'MERA',
         'NIKI',
         'CF',
         'SP',
         'PollingFirm',
         'Commissioner',
         'Fieldwork date_Original',
         'Noise_level']]

#Some small corrections
#df = df.fillna(0)
#infered_polling_small_parties['stdv_GREEKS'] = 0
#infered_polling_small_parties['mean_GREEKS'].loc[infered_polling_small_parties['mean_GREEKS']<0] = 0

df.to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023-06-25_election/polling_data.csv', index=False)
infered_polling.to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023-06-25_election/infered_polling.csv', index=False)
infered_polling_small_parties.to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023-06-25_election/infered_polling_small_parties.csv', index=False)


bias_matrix = bias_matrix.rename(columns={
    "Movement for Change": "KINAL",
    "New Democracy": "ND",
    "Communist Party of Greece": "KKE",
    "Coalition of the Left": "SYRIZA",
    "Greek Solution": "EL",
    "European Realistic Disobedience Front": "MERA",
    "Course of Freedom": "CF",
    "Niki": "NIKI",
    "Spartans": "SP",
                   })
bias_matrix_commissioner = bias_matrix_commissioner.rename(columns={
    "Movement for Change": "KINAL",
    "New Democracy": "ND",
    "Communist Party of Greece": "KKE",
    "Coalition of the Left": "SYRIZA",
    "Greek Solution": "EL",
    "European Realistic Disobedience Front": "MERA",
    "Course of Freedom": "CF",
    "Niki": "NIKI",
    "Spartans": "SP",
                   })

bias_matrix.dropna(axis=0).to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023-06-25_election/bias_matrix.csv',index_label='Pollster')
bias_matrix_commissioner.dropna(axis=0).to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023-06-25_election/bias_matrix_commissioner.csv',index_label='Commissioner')


end = 1




