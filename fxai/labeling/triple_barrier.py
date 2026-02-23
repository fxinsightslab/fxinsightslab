import pandas as pd


def triple_barrier(
    close: pd.Series,
    atr: pd.Series,
    k_up: float,
    k_dn: float,
    n_bars: int,
    event_window: int | None = None,
) -> pd.DataFrame:
    """Triple-Barrierラベルを生成する。"""
    horizon = int(event_window or n_bars)
    records: list[dict] = []

    for idx in range(len(close)):
        end = min(idx + horizon, len(close) - 1)
        if idx >= len(close) - 1:
            records.append({"label_direction": 0, "label_success": 0, "label_t_bar": 0, "label_up_bar": 0, "label_down_bar": 0})
            continue

        entry = close.iloc[idx]
        band = atr.iloc[idx]
        if pd.isna(entry) or pd.isna(band):
            records.append({"label_direction": 0, "label_success": 0, "label_t_bar": 0, "label_up_bar": 0, "label_down_bar": 0})
            continue

        up = entry + k_up * band
        down = entry - k_dn * band

        up_hit = 0
        down_hit = 0
        t_bar = end - idx

        for step in range(1, end - idx + 1):
            px = close.iloc[idx + step]
            if px >= up:
                up_hit = step
                t_bar = step
                break
            if px <= down:
                down_hit = step
                t_bar = step
                break

        direction = 1 if up_hit > 0 else (-1 if down_hit > 0 else 0)
        success = 1 if direction != 0 else 0
        records.append(
            {
                "label_direction": direction,
                "label_success": success,
                "label_t_bar": int(t_bar),
                "label_up_bar": int(up_hit),
                "label_down_bar": int(down_hit),
            }
        )

    return pd.DataFrame.from_records(records, index=close.index)
