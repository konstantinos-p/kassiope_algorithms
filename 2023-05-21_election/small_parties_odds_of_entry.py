from analysis_utils import compute_all_bias, remove_defunct_parties, compute_regression, debias
import pandas as pd
from greece.seat_allocation import odds_of_entry
import numpy as np

df = pd.read_csv('new_polls_kasidiaris.csv')
df = remove_defunct_parties(df)
bias_matrix = compute_all_bias(df.copy())
bias_matrix_commissioner = compute_all_bias(df.copy(), agent='Commissioner')
debiased_df = debias(df.copy(), bias_matrix)
df_reg = compute_regression(debiased_df, start_date='2019-07-07', end_date='2023-05-21')

#Some small modifications
df_reg['Date'] = pd.to_datetime(df_reg['Date']).dt.date
df['Date'] = pd.to_datetime(df['Date']).dt.date

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
    "National Party - Greeks_mean": "mean_GREEKS",
    "National Party - Greeks_std": "stdv_GREEKS",
    "Date": "date",
                   })

probs = []
parties = ['ND', 'SYRIZA', 'KINAL', 'KKE', 'EL', 'MERA', 'GREEKS']
for party in parties:

    probs.append(odds_of_entry(polling_mean=df_reg.loc[df_reg['date'].max() == df_reg['date']]['mean_'+party],
                                polling_std=df_reg.loc[df_reg['date'].max() == df_reg['date']]['stdv_'+party]
                               ))
probs = np.array(probs)
probs = np.reshape(probs, (1, -1))
odds_df = pd.DataFrame(probs, columns=parties)
odds_df.to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023_election/odds_df.csv', index=False)

end=1




