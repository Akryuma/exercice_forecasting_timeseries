import pandas as pd
import numpy as np
from typing import Literal

def add_str_dates(raw_data: pd.DataFrame, unit: Literal["s","m", "h", "d"] = "m") -> pd.DataFrame:
    data = raw_data.copy()
    # Convert the timestamp to seconds, minutes, hours or days
    if unit == "s":
        data["timestamp"] = data.apply(lambda row: row["timestamp"]/1000, axis=1,)
    elif unit == "m":
        data["timestamp"] = data.apply(lambda row: row["timestamp"]/1000/60, axis=1,)
    elif unit == "h":
        data["timestamp"] = data.apply(lambda row: row["timestamp"]/1000/60/60, axis=1,)
    elif unit == "d":
        data["timestamp"] = data.apply(lambda row: row["timestamp"]/1000/60/60/24, axis=1,)
    else:
        raise NotImplementedError(f"Unit {unit} not implemented")
    data["datetime"] = pd.to_datetime(data["timestamp"], unit=unit)
    data.sort_values('datetime', inplace=True)
    data.set_index("datetime", inplace=True, drop=False)
    return data

def add_returns(data: pd.DataFrame) -> pd.DataFrame:
    # Drop duplicate timestamps if any
    data.drop_duplicates("timestamp", inplace=True)

    # Mark the session break (weekends)
    # Threshold 5 min / 300 s (time gap) * 5 
    date_gap = data.index.to_series().diff().dt.total_seconds()
    data["session_break"] = (date_gap > 300 * 5)

    # Compute returns & vols by session
    data["session_id"] = data["session_break"].cumsum()
    data["log_close"] = np.log(data["close"])
    data["returns"] = data.groupby('session_id')["log_close"].diff()
    data.loc[data.index[0], "returns"] = 0.0  # first return is Nan, set to 0

    

    # Outlier cleaning
    window = 50
    data["z_score"] = (data["returns"] - data["returns"].rolling(window).mean()) / data["returns"].rolling(window).std()

    threshold_zscore = 10
    data.loc[np.abs(data["z_score"]) > threshold_zscore, "returns"] = np.nan
    data["returns"] = data["returns"].interpolate(method='linear')
    return data

def resample_frequency(data: pd.DataFrame, frequency = "1d") -> pd.DataFrame:
    data["one_var"] = data.apply(lambda row: np.log(row["high"]/row["low"])**2/(4*np.log(2)), axis=1) # Parkinson's volatility estimator
    def aggregate_session(df: pd.DataFrame) -> pd.Series:
        if df.empty:
            return
        return pd.Series({
            "timestamp": df["timestamp"].iloc[0],
            "datetime": df["datetime"].iloc[0],
            "open": df["open"].iloc[0],
            "high": df["high"].max(),
            "low": df["low"].min(),
            "close": df["close"].iloc[-1],
            "volume": df["volume"].sum(),
            "var": df["one_var"].mean(),
            "vol": np.sqrt(df["one_var"].mean()),
            "session_break": df["session_break"].iloc[0],
            "session_id": df["session_id"].iloc[0],
            "returns": df["returns"].sum()
        })

    resampled_data = data.resample(frequency).apply(aggregate_session)
    resampled_data.dropna(inplace=True)
    return resampled_data