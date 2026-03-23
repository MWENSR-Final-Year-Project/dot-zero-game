from unittest.mock import patch
import pytest
from agents import HeuristicAgent
from game import Move, GameState


class DummyState:
    def __init__(self, moves,):
        self._moves = moves

    def get_legal_moves(self):
        return self._moves


def test_raises_when_no_legal_moves():
    with pytest.raises(ValueError):
        HeuristicAgent().select_move(DummyState([]))


def test_takes_box_completing_move():
    m1, m2 = Move("H", 0, 0), Move("V", 0, 0)
    state = DummyState([m1, m2])

    with patch("agents.heuristic_agent.boxes_completed_by") as mock:
        mock.side_effect = lambda _, m: 1 if m == m2 else 0
        chosen = HeuristicAgent().select_move(state)

    assert chosen == m2


def test_prefers_safe_move():
    m1, m2 = Move("H", 0, 0), Move("V", 0, 0)
    state = DummyState([m1, m2])

    with (
        patch("agents.heuristic_agent.boxes_completed_by", return_value=0),
        patch("agents.heuristic_agent.creates_third_edge") as mock,
    ):
        mock.side_effect = lambda _, m: m == m1
        chosen = HeuristicAgent().select_move(state)

    assert chosen == m2


def test_minimises_boxes_given_to_opponent():
    m1, m2 = Move("H", 0, 0), Move("V", 0, 0)
    state = DummyState([m1, m2])

    with (
        patch("agents.heuristic_agent.boxes_completed_by", return_value=0),
        patch("agents.heuristic_agent.creates_third_edge", return_value=True),
        patch("agents.heuristic_agent.boxes_given_to_opponent") as mock,
    ):
        mock.side_effect = lambda _, m: 3 if m == m1 else 1
        chosen = HeuristicAgent().select_move(state)

    assert chosen == m2