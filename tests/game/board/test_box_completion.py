import numpy as np
import pytest
from game import Board, Move


def test_box_completed_true():
    board = Board(size=3)
    r, c = 1, 1
    board.horizontal_edges[r, c] = 1
    board.horizontal_edges[r + 1, c] = 1
    board.vertical_edges[r, c] = 1
    board.vertical_edges[r, c + 1] = 1
    assert board.is_box_completed(r, c) is np.True_


@pytest.mark.parametrize("missing_edge", ["left", "right"])
def test_box_not_completed_missing_vertical_edge(missing_edge):
    board = Board(size=3)
    r, c = 1, 0
    board.horizontal_edges[r, c] = 1
    board.horizontal_edges[r + 1, c] = 1
    if missing_edge == "left":
        board.vertical_edges[r, c + 1] = 1
    else:
        board.vertical_edges[r, c] = 1
    assert board.is_box_completed(r, c) is np.False_


@pytest.mark.parametrize("missing_edge", ["up", "down"])
def test_box_not_completed_missing_horizontal_edge(missing_edge):
    board = Board(size=3)
    r, c = 1, 0
    board.vertical_edges[r, c] = 1
    board.vertical_edges[r, c + 1] = 1
    if missing_edge == "up":
        board.horizontal_edges[r + 1, c] = 1
    else:
        board.horizontal_edges[r, c] = 1
    assert board.is_box_completed(r, c) is np.False_


def test_horizontal_move_completes_top_box():
    board = Board(size=3)
    board.horizontal_edges[0, 1] = 1
    board.vertical_edges[0, 1] = 1
    board.vertical_edges[0, 2] = 1
    move = Move("H", row=1, col=1)
    board.horizontal_edges[1, 1] = 1
    assert board.get_completed_boxes(move) == [(0, 1)]


def test_horizontal_move_completes_bottom_box():
    board = Board(size=3)
    board.horizontal_edges[2, 0] = 1
    board.vertical_edges[1, 0] = 1
    board.vertical_edges[1, 1] = 1
    move = Move("H", row=1, col=0)
    board.horizontal_edges[1, 0] = 1
    assert board.get_completed_boxes(move) == [(1, 0)]


def test_horizontal_move_completes_two_boxes():
    board = Board(size=3)
    board.horizontal_edges[0, 1] = 1
    board.vertical_edges[0, 1] = 1
    board.vertical_edges[0, 2] = 1
    board.horizontal_edges[2, 1] = 1
    board.vertical_edges[1, 1] = 1
    board.vertical_edges[1, 2] = 1
    move = Move("H", row=1, col=1)
    board.horizontal_edges[1, 1] = 1
    assert set(board.get_completed_boxes(move)) == {(0, 1), (1, 1)}


def test_vertical_move_completes_left_box():
    board = Board(size=3)
    board.vertical_edges[1, 0] = 1
    board.horizontal_edges[1, 0] = 1
    board.horizontal_edges[2, 0] = 1
    move = Move("V", row=1, col=1)
    board.vertical_edges[1, 1] = 1
    assert board.get_completed_boxes(move) == [(1, 0)]


def test_vertical_move_completes_right_box():
    board = Board(size=3)
    board.vertical_edges[1, 2] = 1
    board.horizontal_edges[1, 1] = 1
    board.horizontal_edges[2, 1] = 1
    move = Move("V", row=1, col=1)
    board.vertical_edges[1, 1] = 1
    assert board.get_completed_boxes(move) == [(1, 1)]


def test_vertical_move_completes_two_boxes():
    board = Board(size=3)
    board.vertical_edges[1, 0] = 1
    board.horizontal_edges[1, 0] = 1
    board.horizontal_edges[2, 0] = 1
    board.vertical_edges[1, 2] = 1
    board.horizontal_edges[1, 1] = 1
    board.horizontal_edges[2, 1] = 1
    move = Move("V", row=1, col=1)
    board.vertical_edges[1, 1] = 1
    assert set(board.get_completed_boxes(move)) == {(1, 0), (1, 1)}