from analysis_utils import compute_all_bias, remove_defunct_parties, debias, compute_regression
from advanced_analysis_utils import sample_from_student_t
import pandas as pd
from greece.seat_allocation import seat_projection_with_bonus, get_seats_per_division_single_sample
import numpy as np

df = pd.read_csv('new_polls.csv')
df = remove_defunct_parties(df)
bias_matrix = compute_all_bias(df.copy())
debiased_df = debias(df.copy(), bias_matrix)
df_reg = compute_regression(debiased_df, start_date='2023-06-25', end_date='2027-06-25')
df_reg = df_reg[df_reg.columns.drop(list(df_reg.filter(regex='_std')))]
df_reg.columns = df_reg.columns.str.replace(r'_mean$', '')
party_map = {
    'New Democracy': 'ND',
    'Movement for Change': 'PASOK',
    'Communist Party of Greece': 'KKE',
    'European Realistic Disobedience Front': 'MERA25',
    'Coalition of the Left': 'SYRIZA',
    'Greek Solution': 'EL',
    'Niki': 'MERA25',
    'Course of Freedom': 'MERA25',
    'Spartans': 'MERA25',
}
historical_data = pd.read_csv('/Users/pkonstan/PycharmProjects/advanced_europepolls_party_analysis/countries/greece/polls_elections_diff.csv')
samples = sample_from_student_t(df_reg.copy(),
                                party_map=party_map,
                                historical_data=historical_data,
                                num_samples=10000)
seats = seat_projection_with_bonus(samples.copy())

path_to_assets = '/Users/pkonstan/PycharmProjects/per_country_poll_analysis/greece/assets/'
list_seats_per_division = []
for i in range(len(samples)):
    seats_per_division = get_seats_per_division_single_sample(national_polling_results=samples.iloc[[i]],
                                                          path_to_assets=path_to_assets,
                                                          new_parties={
                                                                       'Spartans': 'Νίκη'
                                                                       },
                                                          rename={'Νέα Δημοκρατία': 'New Democracy',
                                                                  'ΣΥΡΙΖΑ': 'Coalition of the Left',
                                                                  'ΚΙΝΑΛ': 'Movement for Change',
                                                                  'ΚΚΕ': 'Communist Party of Greece',
                                                                  'Ελληνική Λύση': 'Greek Solution',
                                                                  'Μέρα25': 'European Realistic Disobedience Front',
                                                                  'Πλεύση Ελευθερίας': 'Course of Freedom',
                                                                  'Νίκη': 'Niki',
                                                                  'Σπαρτιάτες': 'Spartans'
                                                                  },
                                                           proportional=False)#'Χρυσή Αυγή': 'National Party - Greeks'
    list_seats_per_division.append(seats_per_division.copy().to_numpy())

max_seats = 10
sum = np.zeros(shape=list_seats_per_division[0].shape+(max_seats,))
arange_tensor = np.expand_dims(np.ones(shape=list_seats_per_division[0].shape), axis=2)*np.expand_dims(np.arange(max_seats),axis=0)
for seats in list_seats_per_division:
    tmp = arange_tensor - np.expand_dims(seats, axis=2)*np.expand_dims(np.ones(max_seats), axis=0)
    sum[np.where(tmp < 0)] += 1

shape_rec = sum.shape
final_seats = np.zeros(shape_rec)
final_seats = final_seats.flatten()
sum = sum.flatten()
index = np.argsort(sum)
final_seats[index[-300:]] += 1
final_seats = final_seats.reshape(shape_rec).sum(axis=2)
final_seats_df = seats_per_division.copy()
final_seats_df.loc[:] = final_seats

total_pred_seats_per_party = final_seats.sum(axis=1)
total_allocated_seats = final_seats.sum()

final_seats_df = final_seats_df.transpose()
final_seats_df = final_seats_df.rename(columns={
    "Movement for Change": "KINAL",
    "New Democracy": "ND",
    "Communist Party of Greece": "KKE",
    "Coalition of the Left": "SYRIZA",
    "Greek Solution": "EL",
    "European Realistic Disobedience Front": "MERA",
    'Course of Freedom': 'CF',
    'Niki': 'NIKI',
    'Spartans': 'SP',
                   }) # "National Party - Greeks": "GREEKS",
final_seats_df.loc['Σύνολο'] = final_seats_df.sum()
final_seats_df.reset_index(inplace=True)
final_seats_df = final_seats_df.rename(columns={'index': 'Divisions'})
final_seats_df.to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2027-06-25_election/seats_per_division.csv', index=False)

end = 1
