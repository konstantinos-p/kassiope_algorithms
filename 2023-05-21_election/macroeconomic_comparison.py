from main_m import get_current_predictions
import pandas as pd
import os
from datetime import date
from polls import get_recent_polls

current_dir = os.getcwd()
os.chdir('/Users/pkonstan/PycharmProjects/macroeconomic_data_api')
df = get_current_predictions(country='greece')
os.chdir(current_dir)

today = date.today()


name_change_kassiope_tmp = {
    "Movement for Change": "KINAL",
    "New Democracy": "ND",
    "Communist Party of Greece": "KKE",
    "Coalition of the Left": "SYRIZA",
    "Greek Solution": "EL",
    "European Realistic Disobedience Front": "MERA",
                   }
# Swap keys and values of dictionary
name_change_kassiope = {v: k for k, v in name_change_kassiope_tmp.items()}

# Get party_id
df_dummy, party_id = get_recent_polls('greece', from_date='2019-07-07', party_id=True)

for i in name_change_kassiope.keys():
    for j in party_id.keys():
        if name_change_kassiope[i] == j:
            name_change_kassiope[i] = party_id[j]


big_parties = pd.read_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023_election/infered_polling.csv')
small_parties = pd.read_csv('/Users/pkonstan/PycharmProjects/kassiope/assets/data/polling_2023_election/infered_polling_small_parties.csv')



end = 1
