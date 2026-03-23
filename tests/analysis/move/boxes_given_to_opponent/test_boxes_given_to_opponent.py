import pytest
from analysis.move import boxes_given_to_opponent
from game import Board, GameState, Move


@pytest.mark.parametrize(
    "setup_moves, losing_move, expected",
    [
        (
            [],
            Move("H", 0, 0),
            0,
        ),
        (
            [
                Move("H", 0, 0),
                Move("V", 0, 0),
            ],
            Move("V", 0, 1),
            1,
        ),
        (
            [
                Move("H", 0, 0),
                Move("H", 0, 1),
                Move("H", 1, 0),
                Move("H", 1, 1),
                Move("H", 2, 0),
                Move("H", 2, 1),
                Move("V", 1, 0),
                Move("V", 1, 1),
                Move("V", 1, 2),
            ],
            Move("V", 0, 1),
            2,
        ),
        (
            [
                Move("H", 0, 0),
                Move("H", 0, 1),
                Move("H", 1, 0),
                Move("H", 2, 0),
                Move("H", 2, 1),
                Move("V", 1, 0),
                Move("V", 1, 1),
                Move("V", 1, 2),
            ],
            Move("V", 0, 1),
            3,
        ),
        (
            [
                Move("H", 0, 0),
                Move("H", 0, 1),
                Move("H", 1, 0),
                Move("H", 2, 0),
                Move("H", 2, 1),
                Move("V", 1, 0),
                Move("V", 1, 2),
            ],
            Move("V", 0, 1),
            4,
        ),
    ],
)
def test_boxes_given_to_opponent(
    setup_moves,
    losing_move,
    expected,
):
    state = GameState(Board(size=2))

    for move in setup_moves:
        state = state.apply_move(move)

    assert boxes_given_to_opponent(state, losing_move) == expected
