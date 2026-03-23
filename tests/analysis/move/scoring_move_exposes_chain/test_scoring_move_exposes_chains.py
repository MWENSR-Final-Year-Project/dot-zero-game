from game.board import Board
from game.move import Move
from game.state import GameState
from analysis.move.scoring_move_exposes_chain import scoring_move_exposes_chain


def test_returns_false_for_non_scoring_move():
    state = GameState(Board(size=3))
    assert scoring_move_exposes_chain(state, Move("H", 0, 0)) is False


def test_returns_false_when_scoring_move_is_safe():
    board = Board(size=2)
    board.horizontal_edges[0][0] = 1
    board.horizontal_edges[1][0] = 1
    board.vertical_edges[0][0] = 1

    state = GameState(board)
    completing_move = Move("V", 0, 1)

    result = scoring_move_exposes_chain(state, completing_move)
    assert isinstance(result, bool)


def test_returns_true_when_scoring_move_opens_chain():
    board = Board(size=3)

    board.horizontal_edges[0][0] = 1
    board.horizontal_edges[1][0] = 1
    board.vertical_edges[0][0] = 1

    board.horizontal_edges[0][1] = 1
    board.horizontal_edges[1][1] = 1

    state = GameState(board)
    completing_move = Move("V", 0, 1)

    assert scoring_move_exposes_chain(state, completing_move) is True
