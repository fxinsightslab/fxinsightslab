import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ("ts", "o", "h", "l", "c", "v", "spread")
NUMERIC_COLUMNS = ("o", "h", "l", "c", "v", "spread")
OUTPUT_COLUMNS = ("symbol", "ts_utc", "o", "h", "l", "c", "v", "spread", "session")


def _validate_required_columns(df: pd.DataFrame) -> None:
    """必須カラム不足を検出する。"""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        message = f"missing required columns: {missing_text}"
        logger.error(message)
        raise ValueError(message)


def _parse_ts_to_utc(ts_series: pd.Series) -> pd.Series:
    """時刻列をUTCに正規化し、naive時刻を拒否する。"""
    parsed_list = []
    for value in ts_series:
        ts = pd.Timestamp(value)
        if ts.tzinfo is None:
            message = "timestamp must be tz-aware: found naive ts"
            logger.error(message)
            raise ValueError(message)
        parsed_list.append(ts.tz_convert("UTC"))
    return pd.Series(parsed_list, index=ts_series.index, dtype="datetime64[ns, UTC]")


def _coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """数値列を厳密変換し、失敗時は例外化する。"""
    converted = df.copy()
    for column in NUMERIC_COLUMNS:
        try:
            converted[column] = pd.to_numeric(converted[column], errors="raise")
        except Exception as exc:
            message = f"numeric conversion failed for column: {column}"
            logger.error(message)
            raise ValueError(message) from exc
    return converted


def _build_session(ts_utc: pd.Series) -> pd.Series:
    """UTC時刻帯から簡易セッションを付与する。"""
    hours = ts_utc.dt.hour
    session = pd.Series("asia", index=ts_utc.index, dtype="string")
    session[(hours >= 7) & (hours < 16)] = "london"
    session[(hours >= 13) & (hours < 22)] = "newyork"
    return session


def load_mt5(symbol: str, timeframe: str, input_path: str | Path) -> pd.DataFrame:
    """MT5/CSV入力を読み込み、Data Contract準拠のDFを返す。"""
    df = pd.read_csv(input_path)
    _validate_required_columns(df)
    df = _coerce_numeric_columns(df)
    df["ts_utc"] = _parse_ts_to_utc(df["ts"])
    df["symbol"] = symbol
    df["session"] = _build_session(df["ts_utc"])
    df = df.sort_values("ts_utc", kind="mergesort").reset_index(drop=True)

    if df["ts_utc"].duplicated().any():
        message = "duplicate ts_utc detected"
        logger.error(message)
        raise ValueError(message)

    if timeframe != "M1":
        message = f"unsupported timeframe for loader: {timeframe}"
        logger.error(message)
        raise ValueError(message)

    return df.loc[:, OUTPUT_COLUMNS]
