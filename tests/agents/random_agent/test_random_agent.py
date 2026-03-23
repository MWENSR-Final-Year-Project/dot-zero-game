import pytest
from agents import RandomAgent
from game import Board, GameState


def test_random_agent_returns_legal_move():
    board = Board(size=2)
    state = GameState(board)
    agent = RandomAgent()

    move = agent.select_move(state)

    assert move in state.get_legal_moves()


def test_random_agent_raises_when_no_legal_moves():
    board = Board(size=1)
    state = GameState(board)

    for move in state.get_legal_moves():
        state.board.add_edge(move)

    agent = RandomAgent()

    with pytest.raises(ValueError):
        agent.select_move(state)
