from unittest.mock import patch
import pytest
from agents.base_agent import Agent
from game.move import Move


class ConcreteAgent(Agent):
    def __init__(self):
        super().__init__("Concrete")
        self.fallback_called_with = None

    def _fallback(self, state, legal_moves, safe_moves):
        self.fallback_called_with = (legal_moves, safe_moves)
        return legal_moves[0]


class DummyState:
    def __init__(self, moves):
        self._moves = moves

    def get_legal_moves(self):
        return self._moves


def test_raises_when_no_legal_moves():
    with pytest.raises(ValueError, match="Concrete"):
        ConcreteAgent().select_move(DummyState([]))


def test_returns_best_scoring_move():
    m1, m2 = Move("H", 0, 0), Move("V", 0, 0)
    state = DummyState([m1, m2])
    agent = ConcreteAgent()

    with patch("agents.base_agent.boxes_completed_by") as mock:
        mock.side_effect = lambda _, m: 2 if m == m2 else 0
        chosen = agent.select_move(state)

    assert chosen == m2


def test_calls_fallback_when_no_scoring_move():
    m1, m2 = Move("H", 0, 0), Move("V", 0, 0)
    state = DummyState([m1, m2])
    agent = ConcreteAgent()

    with (
        patch("agents.base_agent.boxes_completed_by", return_value=0),
        patch("agents.base_agent.creates_third_edge", return_value=False),
    ):
        agent.select_move(state)

    assert agent.fallback_called_with is not None


def test_safe_moves_exclude_third_edge_moves():
    m1, m2 = Move("H", 0, 0), Move("V", 0, 0)
    state = DummyState([m1, m2])
    agent = ConcreteAgent()

    with (
        patch("agents.base_agent.boxes_completed_by", return_value=0),
        patch("agents.base_agent.creates_third_edge") as mock,
    ):
        mock.side_effect = lambda _, m: m == m1
        agent.select_move(state)

    _, safe_moves = agent.fallback_called_with
    assert m1 not in safe_moves
    assert m2 in safe_moves
