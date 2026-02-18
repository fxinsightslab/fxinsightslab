from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import random


@dataclass
class QLearningConfig:
    bins: int = 7
    lr: float = 0.08
    gamma: float = 0.98
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    epsilon_decay: float = 0.995


class QLearningAgent:
    def __init__(self, state_dim: int, action_dim: int = 3, config: QLearningConfig | None = None) -> None:
        self.cfg = config or QLearningConfig()
        self.state_dim = state_dim
        self.action_dim = action_dim

        self.bin_edges = [self._linspace(-1.0, 1.0, self.cfg.bins - 1) for _ in range(state_dim)]
        self.q = [[0.0 for _ in range(action_dim)] for _ in range(self.cfg.bins**state_dim)]
        self.epsilon = self.cfg.epsilon_start

    def act(self, state: list[float]) -> int:
        if random.random() < self.epsilon:
            return random.randrange(self.action_dim)
        idx = self.state_to_index(state)
        return self._argmax(self.q[idx])

    def greedy_action(self, state: list[float]) -> int:
        idx = self.state_to_index(state)
        return self._argmax(self.q[idx])

    def update(self, state: list[float], action: int, reward: float, next_state: list[float], done: bool) -> None:
        s = self.state_to_index(state)
        ns = self.state_to_index(next_state)
        next_v = 0.0 if done else max(self.q[ns])
        td_target = reward + self.cfg.gamma * next_v
        self.q[s][action] += self.cfg.lr * (td_target - self.q[s][action])

    def decay_epsilon(self) -> None:
        self.epsilon = max(self.cfg.epsilon_end, self.epsilon * self.cfg.epsilon_decay)

    def state_to_index(self, state: list[float]) -> int:
        digits: list[int] = []
        clipped = [min(1.0, max(-1.0, v)) for v in state]
        for i, v in enumerate(clipped):
            d = self._digitize(v, self.bin_edges[i])
            digits.append(d)

        idx = 0
        base = self.cfg.bins
        for d in digits:
            idx = idx * base + d
        return idx

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"q": self.q}, f)

    def load(self, path: str | Path) -> None:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        self.q = payload["q"]

    @staticmethod
    def _linspace(start: float, end: float, points: int) -> list[float]:
        if points <= 0:
            return []
        step = (end - start) / (points + 1)
        return [start + step * (i + 1) for i in range(points)]

    @staticmethod
    def _digitize(value: float, edges: list[float]) -> int:
        idx = 0
        for edge in edges:
            if value > edge:
                idx += 1
            else:
                break
        return idx

    @staticmethod
    def _argmax(values: list[float]) -> int:
        best_idx = 0
        best_val = values[0]
        for i, v in enumerate(values):
            if v > best_val:
                best_val = v
                best_idx = i
        return best_idx
