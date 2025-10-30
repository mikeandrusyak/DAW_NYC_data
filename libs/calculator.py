import pandas as pd

# The Functions in this file are used to perform calculations on the data fetched from the API
def calc_sample_size(data: pd.DataFrame, target_sample_size: int = 10_000): 
    data_with_sample_size = data.copy()
    data_with_sample_size["total"] = pd.to_numeric(data_with_sample_size["total"])

    # Calculate total number and proportions
    total_records = data_with_sample_size["total"].sum()
    print(type(data_with_sample_size["total"]))
    data_with_sample_size["share"] = data_with_sample_size["total"] / total_records

    data_with_sample_size["sample_size"] = (data_with_sample_size["share"] * target_sample_size).round().astype(int)

    # Adjust rounding errors (sum exactly = target_sample_size)
    diff = target_sample_size - data_with_sample_size["sample_size"].sum()
    if diff != 0 and len(data_with_sample_size) > 0:
        data_with_sample_size.loc[data_with_sample_size.index[0], "sample_size"] += diff
    return data_with_sample_size