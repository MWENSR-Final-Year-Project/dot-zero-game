from game.board import Board
from game.move import Move
from game.state import GameState
from analysis.move.least_accessible_move import opponent_accessible_boxes


def test_returns_zero_on_empty_board():
    state = GameState(Board(size=2))
    move = Move("H", 0, 0)
    assert opponent_accessible_boxes(state, move) == 0


def test_counts_boxes_opponent_can_complete():
    board = Board(size=2)
    board.horizontal_edges[0][0] = 1
    board.vertical_edges[0][0] = 1
    board.horizontal_edges[0][1] = 1
    board.vertical_edges[0][2] = 1

    state = GameState(board)
    move = Move("H", 1, 0)
    assert opponent_accessible_boxes(state, move) > 0


def test_prefers_move_with_fewer_accessible_boxes():
    board = Board(size=2)
    board.horizontal_edges[0][0] = 1
    board.vertical_edges[0][0] = 1

    state = GameState(board)
    legal_moves = state.get_legal_moves()

    scores = {m: opponent_accessible_boxes(state, m) for m in legal_moves}
    best = min(scores, key=lambda m: scores[m])

    assert scores[best] == min(scores.values())