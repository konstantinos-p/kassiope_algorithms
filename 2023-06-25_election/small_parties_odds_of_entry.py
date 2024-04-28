from analysis_utils import compute_all_bias, remove_defunct_parties, compute_regression, debias
from advanced_analysis_utils import sample_from_student_t
import pandas as pd

df = pd.read_csv('new_polls.csv')
df = remove_defunct_parties(df)
bias_matrix = compute_all_bias(df.copy())
debiased_df = debias(df.copy(), bias_matrix)
df_reg = compute_regression(debiased_df, start_date='2023-05-21', end_date='2023-06-25')
df_reg = df_reg[df_reg.columns.drop(list(df_reg.filter(regex='_std')))]
df_reg.columns = df_reg.columns.str.replace(r'_mean$', '')

# Compute estimates of final percentages
party_map = {
    'New Democracy': 'ND',
    'Movement for Change': 'PASOK',
    'Communist Party of Greece': 'KKE',
    'European Realistic Disobedience Front': 'MERA25',
    'Coalition of the Left': 'SYRIZA',
    'Greek Solution': 'EL',
    'Niki': 'MERA25',
    'Course of Freedom': 'MERA25',
    'Spartans': 'MERA25'
}
historical_data = pd.read_csv('/Users/pkonstan/PycharmProjects/advanced_europepolls_party_analysis/countries/greece/polls_elections_diff.csv')
samples = sample_from_student_t(df_reg.copy(),
                                party_map=party_map,
                                historical_data=historical_data,
                                num_samples=100000)
max_samples = samples.std()
min_samples = samples.std()
odds_df = samples.applymap(lambda x: 1 if x >= 3 else 0).mean()
odds_df = 100*odds_df.to_frame().T
odds_df = odds_df.rename(columns={
    "Movement for Change": "KINAL",
    "New Democracy": "ND",
    "Communist Party of Greece": "KKE",
    "Coalition of the Left": "SYRIZA",
    "Greek Solution": "EL",
    "European Realistic Disobedience Front": "MERA",
    "Niki": "NIKI",
    "Course of Freedom": "CF",
    "Spartans": "SP"
                   }) # "National Party - Greeks": "GREEKS",
odds_df.to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023-06-25_election/odds_df.csv', index=False)

end=1




