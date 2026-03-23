import pytest
from analysis.box import get_adjacent_boxes
from game import Board, Move


@pytest.mark.parametrize(
    "move,expected_boxes",
    [
        (Move("H", 1, 1), [(0, 1), (1, 1)]),
        (Move("H", 0, 2), [(0, 2)]),
        (Move("H", 3, 2), [(2, 2)]),
        (Move("V", 1, 1), [(1, 0), (1, 1)]),
        (Move("V", 0, 0), [(0, 0)]),
        (Move("V", 2, 3), [(2, 2)]),
    ],
)
def test_get_adjacent_boxes(move, expected_boxes):
    board = Board(size=3)

    boxes = list(get_adjacent_boxes(board, move))

    assert set(boxes) == set(expected_boxes)
