import pytest
from game.board import Board
from game.move import Move


def test_add_horizontal_edge():
    board = Board(size=3)
    move = Move("H", row=1, col=2)
    board.add_edge(move)
    assert board.horizontal_edges[1, 2] == 1


def test_add_vertical_edge():
    board = Board(size=3)
    move = Move("V", row=0, col=1)
    board.add_edge(move)
    assert board.vertical_edges[0, 1] == 1


def test_add_edge_raises_if_already_filled():
    board = Board(size=3)
    move = Move("H", row=0, col=0)
    board.add_edge(move)
    with pytest.raises(ValueError, match="Edge already filled"):
        board.add_edge(move)