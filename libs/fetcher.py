import requests
import pandas as pd
import logging 
import random
import time
from io import StringIO


def calc_k_days(start: str, end: str, k_days: int):
    rng = pd.date_range(pd.to_datetime(start), pd.to_datetime(end), inclusive="left")
    k_days_min = min(k_days, len(rng))
    return pd.Series(rng).sample(n=k_days_min, random_state=random.randint(0, 9999)).dt.date.tolist()


def fetch_month_strat_data(
    BASE_URL: str,
    MAX_TIMEOUT: int,
    selectors: list,
    group_by: str,
    group_by_value: str,
    target: int,
    start: str,
    end: str,
    k_days: int,
    per_day_mult: float = 1.4,
    sleep_seconds: float = 0.3
) -> pd.DataFrame:
    
    days = calc_k_days(start, end, k_days)
    per_day = int((target * per_day_mult) // len(days))
    print(f" Here is the count per day: {per_day}")
    parts = []

    for d in days: 
        # Build of days to fetch
        d0 = f"{d}T00:00:00"; d1 = (pd.to_datetime(d) + pd.Timedelta(days=1)).strftime('%Y-%m-%dT00:00:00')
        print(f"Loading Data for: {d0} and {d1}")

        # Build of querry params
        where_clause = (
            f"created_date between '{d0}' and '{d1}' "
            f"AND {group_by}='{group_by_value}'"
        )
        order = random.choice(["ASC","DESC"]) 
        offset = random.randint(0, 1000)
        params = {
            "$select": ",".join(selectors),
            "$where": where_clause,
            "$limit": per_day,
            "$offset": offset,
            "$order": f"created_date {order}"
        }   
        # Request 
        try:
            resp = requests.get(BASE_URL, params = params, timeout=MAX_TIMEOUT)
            resp.raise_for_status()
            df_part = pd.read_csv(StringIO(resp.text))
            print(f"Loaded Data for: {d0} and {d1} with size {len(df_part)}")
            if not df_part.empty: parts.append(df_part)
        except Exception as e:
            logging.error(f"For {group_by_value}, {d}: {e}")
        time.sleep(sleep_seconds)
    # Concat dataframe
    if not parts:
        logging.warning(f"No parts collected for {group_by}={group_by_value} {start}..{end}")
        return pd.DataFrame()
    df = pd.concat(parts, ignore_index=True).drop_duplicates()
    return df