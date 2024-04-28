import pandas as pd


df = pd.read_csv('seats_per_division_aggressive.csv', index_col=0)

df = df.transpose()
KINAL_df = df['Movement for Change'].loc[df['Movement for Change'] > 0.5]
MERA_df = df['European Realistic Disobedience Front'].loc[df['European Realistic Disobedience Front'] > 0.5]
EllinikiLysi_df = df['Greek Solution'].loc[df['Greek Solution'] > 0.5]
KKE_df = df['Communist Party of Greece'].loc[df['Communist Party of Greece'] > 0.5]

end =1