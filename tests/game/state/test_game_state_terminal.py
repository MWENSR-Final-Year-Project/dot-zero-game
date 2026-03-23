import pytest
from game import Board, GameState


@pytest.mark.parametrize("legal_moves, expected", [
    ([], True),
    ([1], False),
    ([1, 2, 3], False),
])
def test_is_terminal(monkeypatch, legal_moves, expected):
    state = GameState(Board(size=3))
    monkeypatch.setattr(state, "get_legal_moves", lambda: legal_moves)

    assert state.is_terminal() is expected


@pytest.mark.parametrize("scores, expected_winner", [
    ({1: 10, -1: 5}, 1),
    ({1: 3, -1: 8}, -1),
    ({1: 6, -1: 6}, 0),
    ({1: 0, -1: 0}, 0),
])
def test_get_winner(scores, expected_winner):
    state = GameState(Board(size=3))
    state.scores = scores

    assert state.get_winner() == expected_winner