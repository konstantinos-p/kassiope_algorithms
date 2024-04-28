from analysis_utils import compute_all_bias, remove_defunct_parties, debias, compute_regression
from advanced_analysis_utils import sample_from_student_t
import pandas as pd
from greece.seat_allocation import seat_projection_with_bonus


df = pd.read_csv('new_polls.csv')
df = remove_defunct_parties(df)
bias_matrix = compute_all_bias(df.copy())
debiased_df = debias(df.copy(), bias_matrix)
df_reg = compute_regression(debiased_df, start_date='2023-05-21', end_date='2023-06-25')
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
                                num_samples=100000)
seats = seat_projection_with_bonus(samples.copy())



NewDemocracy = seats['New Democracy']
prob_new_democracy = NewDemocracy[NewDemocracy > 150].shape[0]/NewDemocracy.shape[0]

coalition_1 = seats['New Democracy']+seats['Greek Solution']
prob_new_democracy_coalition_1 = coalition_1[coalition_1 > 150].shape[0]/coalition_1.shape[0]

coalition_2 = seats['New Democracy']+seats['Greek Solution']+seats['Movement for Change']
prob_new_democracy_coalition_2 = coalition_2[coalition_2 > 150].shape[0]/coalition_2.shape[0]

coalition_5 = seats['New Democracy']+seats['Movement for Change']
prob_new_democracy_coalition_3 = coalition_5[coalition_5 > 150].shape[0]/coalition_5.shape[0]

SYRIZA = seats['Coalition of the Left']
prob_SYRIZA = SYRIZA[SYRIZA > 150].shape[0]/SYRIZA.shape[0]

coalition_3 = seats['Coalition of the Left']+seats['Movement for Change']
prob_SYRIZA_coalition_1 = coalition_3[coalition_3 > 150].shape[0]/coalition_3.shape[0]

coalition_4 = seats['Coalition of the Left']+seats['European Realistic Disobedience Front']+seats['Movement for Change']
prob_SYRIZA_coalition_2 = coalition_4[coalition_4 > 150].shape[0]/coalition_4.shape[0]

coalition_5 = seats['Coalition of the Left']+seats['European Realistic Disobedience Front']+seats['Movement for Change']+seats['Course of Freedom']
prob_SYRIZA_coalition_3 = coalition_5[coalition_5 > 150].shape[0]/coalition_5.shape[0]


samples_SYRIZA_win = samples[coalition_4 > 150]
seats_SYRIZA_win = seats[coalition_4 > 150]

d = {'probs': [prob_new_democracy,
                                prob_new_democracy_coalition_1,
                                prob_new_democracy_coalition_2,
                                prob_new_democracy_coalition_3,
                                prob_SYRIZA,
                                prob_SYRIZA_coalition_1,
                                prob_SYRIZA_coalition_2,
                                prob_SYRIZA_coalition_3]
     }
probs_of_winning = pd.DataFrame(data=d, index=['Νέα Δημοκρατία',
                               'Νέα Δημοκρατία + Ελληνική Λύση',
                               'Νέα Δημοκρατία + Ελληνική Λύση + ΚΙΝΑΛ',
                               'Νέα Δημοκρατία + ΚΙΝΑΛ',
                               'ΣΥΡΙΖΑ',
                               'ΣΥΡΙΖΑ + ΚΙΝΑΛ',
                               'ΣΥΡΙΖΑ + ΚΙΝΑΛ + ΜΕΡΑ25',
                               'ΣΥΡΙΖΑ + ΚΙΝΑΛ + ΜΕΡΑ25 + Πλεύση'
                              ])
probs_of_winning = probs_of_winning*100
probs_of_winning = probs_of_winning.round(2)
probs_of_winning.reset_index(inplace=True)
probs_of_winning = probs_of_winning.rename(columns={'index': 'Coalitions'})
probs_of_winning.to_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023-06-25_election/probs_of_seat_majority.csv', index=False)

end = 1