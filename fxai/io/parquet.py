from pathlib import Path

import pandas as pd


def to_parquet(df: pd.DataFrame, path: str | Path) -> None:
    """DataFrameをParquetへ保存する。"""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)


def from_parquet(path: str | Path) -> pd.DataFrame:
    """ParquetをDataFrameとして読み込む。"""
    return pd.read_parquet(path)
