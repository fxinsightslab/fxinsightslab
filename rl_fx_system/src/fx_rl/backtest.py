from __future__ import annotations

from pathlib import Path
import math

from .agent import QLearningAgent
from .data import generate_synthetic_close, prepare_market_data
from .env import FXTradingEnv


def run_backtest(model_path: str | Path = "artifacts/q_table.json", seed: int = 99) -> dict:
    close = generate_synthetic_close(n=1500, seed=seed)
    market = prepare_market_data(close)
    env = FXTradingEnv(market.prices, market.features)

    agent = QLearningAgent(state_dim=len(market.features[0]) + 1)
    agent.load(model_path)

    state = env.reset()
    done = False
    rets: list[float] = []

    while not done:
        action = agent.greedy_action(state)
        out = env.step(action)
        state = out.next_state
        done = out.done
        rets.append(out.reward)

    mean_ret = sum(rets) / max(len(rets), 1)
    var = sum((r - mean_ret) ** 2 for r in rets) / max(len(rets), 1)
    std = var**0.5
    sharpe = mean_ret / (std + 1e-9) * math.sqrt(252)

    equity_curve: list[float] = []
    eq = 1.0
    for r in rets:
        eq *= 1.0 + r
        equity_curve.append(eq)

    peak = 0.0
    max_dd = 0.0
    for v in equity_curve:
        peak = max(peak, v)
        dd = (v - peak) / max(peak, 1e-9)
        max_dd = min(max_dd, dd)

    return {
        "total_return": equity_curve[-1] - 1.0 if equity_curve else 0.0,
        "sharpe": sharpe,
        "max_drawdown": max_dd,
        "steps": len(rets),
    }


def main() -> None:
    stats = run_backtest()
    print("Backtest Result")
    for k, v in stats.items():
        print(f"- {k}: {v:.4f}" if isinstance(v, float) else f"- {k}: {v}")


if __name__ == "__main__":
    main()
