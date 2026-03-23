import pytest

from agents import DefensiveAgent
from analysis.move import boxes_completed_by, creates_third_edge
from game import Board, GameState, Move


def _three_sided_board():
    board = Board(size=2)
    board.horizontal_edges[0][0] = 1
    board.horizontal_edges[1][0] = 1
    board.vertical_edges[0][0] = 1
    return board


def test_prefers_scoring_move():
    state = GameState(_three_sided_board())
    move = DefensiveAgent().select_move(state)

    assert boxes_completed_by(state, move) > 0


def test_avoids_third_edge():
    state = GameState(_three_sided_board())
    move = DefensiveAgent().select_move(state)

    assert not creates_third_edge(state, move)


def test_picks_random_when_no_safe_moves():
    board = Board(size=2)
    board.horizontal_edges[:] = 1
    for r in range(board.size - 1):
        board.vertical_edges[r][:] = 1

    move = DefensiveAgent().select_move(GameState(board))

    assert isinstance(move, Move)


def test_raises_when_no_moves():
    board = Board(size=2)
    board.horizontal_edges[:] = 1
    board.vertical_edges[:] = 1

    with pytest.raises(ValueError):
        DefensiveAgent().select_move(GameState(board))