import numpy as np
import pytest
from unittest.mock import MagicMock, patch
from agents import NGMCTSAgent
from agents.base_agent import Agent
from game import Board, GameState


def _make_agent(**kwargs):
    model = MagicMock()
    model.return_value = (MagicMock(), MagicMock())
    device = MagicMock()
    return NGMCTSAgent(model=model, device=device, board_size=2, **kwargs)


def test_is_agent_subclass():
    assert issubclass(NGMCTSAgent, Agent)


def test_name():
    assert _make_agent().name == "ng_mcts"


def test_raises_when_no_legal_moves():
    state = GameState(Board(size=1))
    for move in state.get_legal_moves():
        state.board.add_edge(move)

    with pytest.raises(ValueError):
        _make_agent().select_move(state)


def test_returns_legal_move():
    state = GameState(Board(size=2))

    mock_policy = np.zeros(2 * 2 * 3)
    mock_policy[0] = 1.0

    mock_tree = MagicMock()
    mock_tree.select.return_value = MagicMock()
    mock_tree.get_policy.return_value = mock_policy

    with patch("agents.ng_mcts_agent.PUCT", return_value=mock_tree):
        move = _make_agent(num_simulations=1).select_move(state)

    assert move in state.get_legal_moves()
