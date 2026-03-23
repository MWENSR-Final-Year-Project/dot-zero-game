import pytest
from agents.defensive_agent import DefensiveAgent
from analysis.move import opens_chain, scoring_move_exposes_chain
from game.board import Board
from game.move import Move
from game.state import GameState


def _three_sided_board():
    board = Board(size=2)
    board.horizontal_edges[0][0] = 1
    board.horizontal_edges[1][0] = 1
    board.vertical_edges[0][0] = 1
    return board


def test_raises_when_no_legal_moves():
    board = Board(size=2)
    board.horizontal_edges[:] = 1
    board.vertical_edges[:] = 1

    with pytest.raises(ValueError):
        DefensiveAgent().select_move(GameState(board))


def test_takes_safe_scoring_move():
    state = GameState(_three_sided_board())
    move = DefensiveAgent().select_move(state)
    from analysis.move import boxes_completed_by
    assert boxes_completed_by(state, move) > 0


def test_skips_scoring_move_that_exposes_chain():
    state = GameState(_three_sided_board())
    move = DefensiveAgent().select_move(state)
    assert not scoring_move_exposes_chain(state, move)


def test_avoids_chain_opening_moves():
    state = GameState(Board(size=3))
    move = DefensiveAgent().select_move(state)
    assert not opens_chain(state, move)


def test_falls_back_to_any_move_when_no_safe_moves():
    board = Board(size=2)
    board.horizontal_edges[:] = 1
    for r in range(board.size - 1):
        board.vertical_edges[r][:] = 1

    state = GameState(board)
    move = DefensiveAgent().select_move(state)
    assert isinstance(move, Move)