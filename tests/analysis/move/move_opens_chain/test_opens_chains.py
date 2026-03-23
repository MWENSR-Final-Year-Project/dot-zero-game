from game.board import Board
from game.move import Move
from game.state import GameState
from analysis.move.move_opens_chain import opens_chain


def test_returns_false_on_empty_board():
    state = GameState(Board(size=3))
    assert opens_chain(state, Move("H", 0, 0)) is False


def test_returns_false_when_no_adjacent_two_edge_box():
    board = Board(size=3)
    board.horizontal_edges[0][0] = 1
    state = GameState(board)
    assert opens_chain(state, Move("H", 1, 0)) is False


def test_returns_true_when_move_creates_chain():
    board = Board(size=3)

    board.horizontal_edges[0][0] = 1

    board.horizontal_edges[0][1] = 1
    board.vertical_edges[0][2] = 1

    state = GameState(board)
    assert opens_chain(state, Move("H", 1, 0)) is True


def test_returns_false_when_isolated_two_edge_box():
    board = Board(size=3)

    board.horizontal_edges[0][0] = 1

    state = GameState(board)
    assert opens_chain(state, Move("V", 0, 0)) is False
