import pandas as pd

def prepare_date_time(df):
    df['created_date'] = pd.to_datetime(df['created_date'])
    df['create_month'] = df['created_date'].dt.to_period('M')
    df['create_day'] = df['created_date'].dt.day
    df['closed_date'] = pd.to_datetime(df['closed_date'])
    df['close_month'] = df['closed_date'].dt.to_period('M')
    df['close_day'] = df['closed_date'].dt.day
    return df