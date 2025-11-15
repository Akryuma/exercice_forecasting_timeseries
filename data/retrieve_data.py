from pathlib import Path
import pandas as pd
from .config_data import valid_intervals
from .download_data import download_file

def retrieve_data(underlying, start_date, end_date, interval = "m5"):
    """Retrieve historical data, downloading it if not already present."""
    underlying = underlying.lower()
    if interval not in valid_intervals:
        raise ValueError(f"Interval {interval} not valid. Choose from {valid_intervals}")

    file_name = f"data/raw/{underlying.lower()}_{interval}_{start_date}_{end_date}.csv"
    if not Path(file_name).exists():
        download_file(underlying, start_date, end_date, interval)
    data = pd.read_csv(file_name)
    data.dropna(inplace=True)
    return data