import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = ("ts", "o", "h", "l", "c", "v", "spread")
NUMERIC_COLUMNS = ("o", "h", "l", "c", "v", "spread")
OUTPUT_COLUMNS = ("symbol", "ts_utc", "o", "h", "l", "c", "v", "spread")


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        message = f"missing required columns: {missing_text}"
        logger.error(message)
        raise ValueError(message)


def _parse_ts_to_utc(ts_series: pd.Series) -> pd.Series:
    parsed_ts = pd.to_datetime(ts_series, errors="raise")
    if parsed_ts.dt.tz is None:
        message = "timestamp must be tz-aware: found naive ts"
        logger.error(message)
        raise ValueError(message)
    return parsed_ts.dt.tz_convert("UTC")


def _coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    converted = df.copy()
    for column in NUMERIC_COLUMNS:
        try:
            converted[column] = pd.to_numeric(converted[column], errors="raise")
        except Exception as exc:
            message = f"numeric conversion failed for column: {column}"
            logger.error(message)
            raise ValueError(message) from exc
    return converted


def load_prices_csv(path: str | Path, symbol: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    _validate_required_columns(df)
    df = _coerce_numeric_columns(df)
    df["ts_utc"] = _parse_ts_to_utc(df["ts"])
    df["symbol"] = symbol
    df = df.sort_values("ts_utc", kind="mergesort").reset_index(drop=True)

    if df["ts_utc"].duplicated().any():
        message = "duplicate ts_utc detected"
        logger.error(message)
        raise ValueError(message)

    return df.loc[:, OUTPUT_COLUMNS]
