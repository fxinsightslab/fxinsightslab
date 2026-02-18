from __future__ import annotations

from pathlib import Path
import random

from .agent import QLearningAgent
from .data import generate_synthetic_close, prepare_market_data
from .env import FXTradingEnv


def train(episodes: int = 30, seed: int = 7) -> tuple[QLearningAgent, list[float]]:
    random.seed(seed)

    close = generate_synthetic_close(n=3000, seed=seed)
    market = prepare_market_data(close)
    env = FXTradingEnv(market.prices, market.features)

    agent = QLearningAgent(state_dim=len(market.features[0]) + 1)
    rewards: list[float] = []

    for ep in range(episodes):
        state = env.reset()
        done = False
        ep_reward = 0.0

        while not done:
            action = agent.act(state)
            out = env.step(action)
            agent.update(state, action, out.reward, out.next_state, out.done)
            state = out.next_state
            ep_reward += out.reward
            done = out.done

        agent.decay_epsilon()
        rewards.append(ep_reward)
        if (ep + 1) % 10 == 0:
            print(f"episode={ep+1}, reward={ep_reward:.4f}, epsilon={agent.epsilon:.3f}")

    return agent, rewards


def main() -> None:
    agent, rewards = train()
    model_path = Path("artifacts/q_table.json")
    agent.save(model_path)
    print(f"saved model: {model_path}")
    last10 = rewards[-10:] if len(rewards) >= 10 else rewards
    mean_reward = sum(last10) / max(len(last10), 1)
    print(f"mean reward(last10): {mean_reward:.4f}")


if __name__ == "__main__":
    main()
