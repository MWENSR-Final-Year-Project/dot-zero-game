import pytest
from agents import MCTSAgent
from agents.base_agent import Agent
from game import Board, GameState


def _one_move_left_board():
    board = Board(size=1)
    moves = GameState(board).get_legal_moves()
    for move in moves[:-1]:
        board.add_edge(move)
    return board


def test_is_agent_subclass():
    assert issubclass(MCTSAgent, Agent)


def test_name():
    assert MCTSAgent().name == "pure_mcts"


def test_returns_legal_move():
    state = GameState(Board(size=2))
    move = MCTSAgent(num_simulations=10).select_move(state)
    assert move in state.get_legal_moves()


def test_raises_when_no_legal_moves():
    state = GameState(Board(size=1))
    for move in state.get_legal_moves():
        state.board.add_edge(move)

    with pytest.raises(ValueError):
        MCTSAgent().select_move(state)


def test_raises_on_terminal_state():
    state = GameState(Board(size=1))
    for move in state.get_legal_moves():
        state = state.apply_move(move)

    with pytest.raises(ValueError):
        MCTSAgent().select_move(state)


def test_picks_box_completing_move():
    state = GameState(_one_move_left_board())
    current_player = state.current_player
    new_state = state.apply_move(MCTSAgent(num_simulations=10).select_move(state))
    assert new_state.scores[current_player] > state.scores[current_player]


def test_more_simulations_still_returns_legal_move():
    state = GameState(Board(size=2))
    move = MCTSAgent(num_simulations=200).select_move(state)
    assert move in state.get_legal_moves()
