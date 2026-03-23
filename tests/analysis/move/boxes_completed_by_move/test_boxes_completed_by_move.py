from analysis.move.boxes_completed_by_move import boxes_completed_by
from game import Board, GameState, Move


def test_boxes_completed_by_returns_zero_when_no_box_completed():
    board = Board(size=2)
    state = GameState(board)

    move = state.get_legal_moves()[0]

    assert boxes_completed_by(state, move) == 0


def test_boxes_completed_by_returns_one_when_box_completed():
    board = Board(size=2)

    board.horizontal_edges[0][0] = 1
    board.horizontal_edges[1][0] = 1
    board.vertical_edges[0][0] = 1

    state = GameState(board)

    completing_move = Move("V", 0, 1)

    assert boxes_completed_by(state, completing_move) == 1


def test_boxes_completed_by_returns_multiple_boxes_if_completed():
    board = Board(size=2)

    board.horizontal_edges[0][0] = 1
    board.horizontal_edges[1][0] = 1
    board.horizontal_edges[0][1] = 1
    board.horizontal_edges[1][1] = 1
    board.vertical_edges[0][0] = 1
    board.vertical_edges[0][2] = 1

    state = GameState(board)

    move = Move("V", 0, 1)

    assert boxes_completed_by(state, move) == 2
