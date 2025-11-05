import pandas as pd 
from scipy.stats import chisquare

def test_imported_data_distribution(df):
    df['date'] = pd.to_datetime(df['created_date'])
    df['month'] = df['date'].dt.to_period('M')
    df['day'] = df['date'].dt.day

    bad_months = []
    for month, group in df.groupby('month'):
        counts = group['day'].value_counts().sort_index()
        expected = [counts.mean()] * len(counts)
        _, p = chisquare(counts, expected)
        if p <= 0.05:
            bad_months.append(str(month))
    assert not bad_months, f"Non-uniform daily distribution in months: {bad_months}"