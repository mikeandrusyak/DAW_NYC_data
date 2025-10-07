from io import BytesIO
import pandas as pd 


def parse_csv_to_df(csv_bytes: bytes) -> pd.DataFrame:
    """Parse CSV bytes to DataFrame with proper dtypes."""
    df = pd.read_csv(BytesIO(csv_bytes), dtype=str, na_values=['', 'N/A', 'NULL'])
    
    if df.empty:
        return df
    
    # Parse datetime columns to UTC
    datetime_cols = ['created_date', 'closed_date', 'due_date', 'resolution_action_updated_date']
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)
    
    # Convert coordinate columns to numeric
    numeric_cols = ['latitude', 'longitude', 'x_coordinate_state_plane', 'y_coordinate_state_plane']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Ensure text columns for IDs and zip codes
    text_cols = ['unique_key', 'bbl', 'incident_zip', 'community_board']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)
            df[col] = df[col].replace('nan', None)
    
    return df