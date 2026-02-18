from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StepResult:
    next_state: list[float]
    reward: float
    done: bool
    info: dict


class FXTradingEnv:
    def __init__(
        self,
        prices: list[float],
        features: list[list[float]],
        spread_cost: float = 0.0001,
        overtrade_penalty: float = 0.00005,
    ) -> None:
        if len(prices) != len(features):
            raise ValueError("prices and features length mismatch")
        if len(prices) < 10:
            raise ValueError("insufficient series length")

        self.prices = prices
        self.features = features
        self.spread_cost = spread_cost
        self.overtrade_penalty = overtrade_penalty

        self.t = 0
        self.position = 0
        self.equity = 1.0

    def reset(self) -> list[float]:
        self.t = 0
        self.position = 0
        self.equity = 1.0
        return self._state()

    def step(self, action: int) -> StepResult:
        if action not in (0, 1, 2):
            raise ValueError("invalid action")

        prev_position = self.position
        target_position = {0: self.position, 1: 1, 2: -1}[action]
        changed = target_position != prev_position
        if changed:
            self.position = target_position

        p0 = self.prices[self.t]
        p1 = self.prices[self.t + 1]
        ret = (p1 - p0) / max(p0, 1e-9)

        pnl = self.position * ret
        cost = self.spread_cost if changed else 0.0
        penalty = self.overtrade_penalty if changed else 0.0
        reward = pnl - cost - penalty

        self.equity *= 1.0 + reward
        self.t += 1
        done = self.t >= len(self.prices) - 2

        return StepResult(
            next_state=self._state(),
            reward=float(reward),
            done=done,
            info={"position": self.position, "equity": self.equity, "return": ret, "changed": changed},
        )

    def _state(self) -> list[float]:
        return [*self.features[self.t], float(self.position)]
