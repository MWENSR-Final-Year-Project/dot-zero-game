import pytest

from analysis.box import count_edges_around_box
from game import Board, Move


@pytest.mark.parametrize(
    "edges,expected_count",
    [
        ([], 0),
        ([Move("H", 0, 0)], 1),
        ([Move("H", 0, 0), Move("V", 0, 0)], 2),
        ([Move("H", 0, 0), Move("H", 1, 0), Move("V", 0, 0)], 3),
        ([Move("H", 0, 0), Move("H", 1, 0), Move("V", 0, 0), Move("V", 0, 1)], 4),
    ],
)
def test_count_edges_param(edges, expected_count):
    board = Board(size=2)
    for edge in edges:
        board.add_edge(edge)

    assert count_edges_around_box(board, 0, 0) == expected_count
