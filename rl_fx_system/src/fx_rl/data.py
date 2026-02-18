from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math
import random


@dataclass
class MarketData:
    prices: list[float]
    features: list[list[float]]


def _moving_average(x: list[float], window: int) -> list[float]:
    out: list[float] = []
    for i in range(len(x)):
        start = max(0, i - window + 1)
        chunk = x[start : i + 1]
        out.append(sum(chunk) / len(chunk))
    return out


def _rolling_std(x: list[float], window: int) -> list[float]:
    out: list[float] = []
    for i in range(len(x)):
        start = max(0, i - window + 1)
        chunk = x[start : i + 1]
        mean = sum(chunk) / len(chunk)
        var = sum((v - mean) ** 2 for v in chunk) / len(chunk)
        out.append(var**0.5)
    return out


def _rsi(close: list[float], period: int = 14) -> list[float]:
    deltas = [0.0]
    for i in range(1, len(close)):
        deltas.append(close[i] - close[i - 1])

    gain = [max(d, 0.0) for d in deltas]
    loss = [max(-d, 0.0) for d in deltas]

    avg_gain = [0.0 for _ in close]
    avg_loss = [0.0 for _ in close]
    if len(close) > period:
        avg_gain[period] = sum(gain[1 : period + 1]) / period
        avg_loss[period] = sum(loss[1 : period + 1]) / period

    for i in range(period + 1, len(close)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gain[i]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + loss[i]) / period

    rsi: list[float] = []
    for i in range(len(close)):
        if i < period:
            rsi.append(50.0)
        else:
            rs = avg_gain[i] / (avg_loss[i] + 1e-9)
            rsi.append(100 - (100 / (1 + rs)))
    return rsi


def load_close_from_csv(csv_path: str | Path, close_column: str = "close") -> list[float]:
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        prices = [float(row[close_column]) for row in reader]

    if len(prices) < 50:
        raise ValueError("Need at least 50 rows of close prices")
    return prices


def generate_synthetic_close(n: int = 2000, seed: int | None = 42) -> list[float]:
    rng = random.Random(seed)
    drift = 0.00005
    vol = 0.002
    close: list[float] = []

    price = 100.0
    for _ in range(n):
        r = rng.gauss(drift, vol)
        price = price * math.exp(r)
        close.append(price)
    return close


def build_features(close: list[float]) -> list[list[float]]:
    ret1 = [0.0]
    for i in range(1, len(close)):
        prev = close[i - 1]
        ret1.append((close[i] - prev) / max(prev, 1e-9))

    ma_fast = _moving_average(close, window=10)
    ma_slow = _moving_average(close, window=30)
    ma_gap = [(f - s) / max(c, 1e-9) for f, s, c in zip(ma_fast, ma_slow, close)]
    vol = _rolling_std(ret1, window=20)
    rsi = [v / 100.0 for v in _rsi(close)]

    return [[ret1[i], ma_gap[i], vol[i], rsi[i]] for i in range(len(close))]


def prepare_market_data(close: list[float]) -> MarketData:
    return MarketData(prices=close, features=build_features(close))
