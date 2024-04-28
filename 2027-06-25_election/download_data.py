from polls import get_recent_polls
from analysis_utils import compute_all_bias, remove_defunct_parties, compute_regression, debias
import pandas as pd

df = get_recent_polls('greece', from_date='2019-07-07')
df.to_csv('new_polls.csv')