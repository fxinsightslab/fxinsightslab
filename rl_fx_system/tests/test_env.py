import unittest

from src.fx_rl.agent import QLearningAgent
from src.fx_rl.data import generate_synthetic_close, prepare_market_data
from src.fx_rl.env import FXTradingEnv


class TestFXEnv(unittest.TestCase):
    def setUp(self) -> None:
        close = generate_synthetic_close(n=300, seed=1)
        market = prepare_market_data(close)
        self.env = FXTradingEnv(market.prices, market.features)

    def test_reset_and_step(self):
        state = self.env.reset()
        self.assertEqual(len(state), 5)
        out = self.env.step(1)
        self.assertIn("equity", out.info)

    def test_agent_updates_q(self):
        state = self.env.reset()
        agent = QLearningAgent(state_dim=5)
        action = agent.act(state)
        out = self.env.step(action)

        idx = agent.state_to_index(state)
        before = agent.q[idx][action]
        agent.update(state, action, out.reward, out.next_state, out.done)
        after = agent.q[idx][action]

        self.assertNotEqual(before, after)


if __name__ == "__main__":
    unittest.main()
