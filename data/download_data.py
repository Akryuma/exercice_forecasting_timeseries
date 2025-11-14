import subprocess
from .config_data import valid_intervals, valid_instruments

def download_file(underlying, start_date, end_date, interval = "m5"):
    """Download historical data
    
    Parameters
    ----------
    underlying : str
        The underlying asset symbol (e.g., "EURUSD").
    start_date : str
        The start date for the data in "YYYY-MM-DD" format.
    end_date : str
        The end date for the data in "YYYY-MM-DD" format.
    interval : str, optional
        The time interval for the data (default is "m5" for 5 minutes).
    """

    underlying = underlying.lower()
    if interval not in valid_intervals:
        raise ValueError(f"Invalid interval: {interval}. Valid intervals are: {valid_intervals}")
    if underlying not in valid_instruments:
        raise ValueError(f"Invalid underlying: {underlying}. Valid underlyings are: {valid_instruments}")
    
    cmd = [
        "C:\\Program Files\\nodejs\\npx.cmd", "dukascopy-node",
        "-i", underlying,
        "-from", start_date,
        "-to", end_date,
        "-t", interval,
        "-v", "true",
        "-f", "csv",
        "-dir", "data/raw/",
        "-fn", f"{underlying}_{interval}_{start_date}_{end_date}"
    ]
    try:
        subprocess.run(cmd, check=True)
        print("Success")
    except subprocess.CalledProcessError as e:
        print("Failure")
        raise e