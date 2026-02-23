import sqlite3
from pathlib import Path

import pandas as pd


def sqlite_upsert(table: str, df: pd.DataFrame, db_path: str | Path) -> None:
    """SQLiteへREPLACE方式でUpsertする。"""
    if df.empty:
        return

    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_file) as conn:
        columns = list(df.columns)
        col_defs = ", ".join([f'"{col}" TEXT' for col in columns])
        conn.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({col_defs})')
        placeholders = ", ".join(["?"] * len(columns))
        column_list = ", ".join([f'"{c}"' for c in columns])
        rows = [tuple("" if pd.isna(v) else str(v) for v in row) for row in df[columns].itertuples(index=False, name=None)]
        conn.executemany(
            f'INSERT OR REPLACE INTO "{table}" ({column_list}) VALUES ({placeholders})',
            rows,
        )
        conn.commit()
