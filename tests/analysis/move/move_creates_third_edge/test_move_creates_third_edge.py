import pytest

from analysis.move.move_creates_third_edge import creates_third_edge
from game import Board, GameState, Move


@pytest.mark.parametrize(
    "move,filled_edges,expected",
    [
        (Move("H", 0, 0), [], False),
        (Move("H", 1, 0), [Move("H", 0, 0), Move("V", 0, 0)], True),
        (Move("V", 0, 0), [Move("H", 0, 0), Move("V", 0, 1)], True),
        (Move("V", 1, 1), [], False),
    ],
)
def test_creates_third_edge_param(move, filled_edges, expected):
    board = Board(size=2)
    for edge in filled_edges:
        board.add_edge(edge)

    state = GameState(board)

    assert creates_third_edge(state, move) is expected
