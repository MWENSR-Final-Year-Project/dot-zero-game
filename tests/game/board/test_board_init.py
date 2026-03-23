import numpy as np
from game import Board


def test_horizontal_edge_init():
    board = Board(size=3)
    assert board.horizontal_edges.shape == (4, 3)
    assert board.horizontal_edges.dtype == np.int8
    assert np.all(board.horizontal_edges == 0)


def test_vertical_edge_init():
    board = Board(size=3)
    assert board.vertical_edges.shape == (3, 4)
    assert board.vertical_edges.dtype == np.int8
    assert np.all(board.vertical_edges == 0)


def test_boxes_init():
    board = Board(size=3)
    assert board.boxes.shape == (3, 3)
    assert board.boxes.dtype == np.int8
    assert np.all(board.boxes == 0)
