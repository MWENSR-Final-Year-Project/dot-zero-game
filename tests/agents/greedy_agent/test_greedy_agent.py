import pytest
from agents import GreedyAgent
from analysis.move import boxes_completed_by
from game import Board, GameState


def _three_sided_board():
    board = Board(size=2)
    board.horizontal_edges[0][0] = 1
    board.horizontal_edges[1][0] = 1
    board.vertical_edges[0][0] = 1
    return board


def test_returns_legal_move():
    state = GameState(Board(size=2))
    move = GreedyAgent().select_move(state)
    assert move in state.get_legal_moves()


def test_raises_when_no_legal_moves():
    state = GameState(Board(size=1))
    for move in state.get_legal_moves():
        state.board.add_edge(move)

    with pytest.raises(ValueError):
        GreedyAgent().select_move(state)


def test_picks_box_completing_move():
    state = GameState(_three_sided_board())
    current_player = state.current_player
    new_state = state.apply_move(GreedyAgent().select_move(state))
    assert new_state.scores[current_player] > state.scores[current_player]


def test_picks_move_completing_most_boxes():
    board = Board(size=2)
    board.horizontal_edges[0][0] = 1
    board.horizontal_edges[1][0] = 1
    board.horizontal_edges[0][1] = 1
    board.horizontal_edges[1][1] = 1
    board.vertical_edges[0][0] = 1
    board.vertical_edges[0][2] = 1
    board.horizontal_edges[2][0] = 1
    board.vertical_edges[1][0] = 1

    state = GameState(board)
    legal_moves = state.get_legal_moves()
    max_score = max(boxes_completed_by(state, m) for m in legal_moves)

    assert boxes_completed_by(state, GreedyAgent().select_move(state)) == max_score


def test_falls_back_to_random_when_no_scoring_moves():
    state = GameState(Board(size=2))
    move = GreedyAgent().select_move(state)
    assert move in state.get_legal_moves()