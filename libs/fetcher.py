import requests
import pandas as pd
import logging 
import random
import time
from datetime import datetime
from io import StringIO


# Fetches the data from the API with retries
def fetch_random_sample(
    url: str,
    selectors: list,
    group_value: str,
    group_by: str,
    time_start: str,
    time_end: str,
    sample_size: int,
    multiplier: int = 2
) -> pd.DataFrame:
    
    logging.info(f"Fetching random sample of {sample_size} for {group_by}={group_value} between {time_start} and {time_end}")
    limit = sample_size * multiplier

    offset = random.randint(0, 10_000)
    order_dir = random.choice(["ASC", "DESC"])


    where_clause = (
        f"created_date between '{time_start}' and '{time_end}' "
        f"AND {group_by}='{group_value}'"
    )

    params = {
        "$select": ",".join(selectors),
        "$where": where_clause,
        "$limit": limit,
        "$offset": offset,
        "$order": f"created_date {order_dir}"
    }
    
    # API Call with Error Handling
    try: 
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        df = pd.read_csv(StringIO(resp.text))
    except Exception as e:
        logging.error(f"Error fetching random sample for {group_by}={group_value} between {time_start} and {time_end}: {e}")
        return None

    # Take local random sample
    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=random.randint(0, 9999))

    return df

def fetch_all_samples_from_plan(
    df_plan: pd.DataFrame,
    BASE_URL: str,
    selectors: list,
    group_by: str,
    time_start: str,
    time_end: str,
    sleep_seconds: float = 0.3
) -> pd.DataFrame:
    
    all_samples = []

    for _, row in df_plan.iterrows():
        group_value = row[group_by]
        n = int(row["sample_size"])

        print(f"📥 Loading {n} rows for {group_by} = '{group_value}' ...")

        try: 
            df_sample = fetch_random_sample(
                url=BASE_URL,
                selectors=selectors,
                group_value=group_value,
                group_by=group_by,
                time_start=time_start,
                time_end=time_end,
                sample_size=n
            )

            df_sample[group_by] = group_value  # Safety: ensure column exists
            all_samples.append(df_sample)

            print(f"{len(df_sample)} rows loaded.")
        except Exception as e:
            print(f"Error with {group_value}: {e}")

        time.sleep(sleep_seconds)  # small pause to avoid API rate limit

    if not all_samples:
        return pd.DataFrame()

    return pd.concat(all_samples, ignore_index=True)

 
def fetch_count_of_grouping(url: str, group_by: str, time_start: str, time_end: str) -> pd.DataFrame:
    logging.info(f"Fetching count of grouping {group_by} between {time_start} and {time_end}")
    params = {
            "$select": f"{group_by}, count(*) as total",
            "$where": f"created_date between '{time_start}' and '{time_end}'",
            "$group": group_by,
    }
    try:
        resp = requests.get(url, params=params)
        df_counts = pd.read_csv(StringIO(resp.text))
        return df_counts
    except Exception as e:
        logging.error(
            f"Error fetching count of grouping {group_by} between {time_start} and {time_end}: {e}"
        )
        return None
    