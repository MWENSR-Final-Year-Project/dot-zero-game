import pytest
from game import Move, move_to_index, index_to_move, num_actions, legal_moves_mask


class DummyBoard:
    def __init__(self, size):
        self.size = size


class DummyState:
    def __init__(self, size, legal_moves):
        self.board = DummyBoard(size)
        self._legal_moves = legal_moves

    def get_legal_moves(self):
        return self._legal_moves


@pytest.mark.parametrize("n", [2, 3, 4])
def test_move_index_round_trip(n):
    for index in range(num_actions(n)):
        assert move_to_index(index_to_move(index, n), n) == index


def test_no_duplicate_indices():
    n = 3
    seen = set()

    for row in range(n + 1):
        for col in range(n):
            idx = move_to_index(Move("H", row, col), n)
            assert idx not in seen
            seen.add(idx)

    for row in range(n):
        for col in range(n + 1):
            idx = move_to_index(Move("V", row, col), n)
            assert idx not in seen
            seen.add(idx)

    assert len(seen) == 2 * n * (n + 1)


def test_first_and_last_indices():
    n = 3
    total = num_actions(n)

    assert move_to_index(index_to_move(0, n), n) == 0
    assert move_to_index(index_to_move(total - 1, n), n) == total - 1


def test_legal_moves_mask():
    n = 2
    moves = [Move("H", 0, 0), Move("V", 1, 0)]
    mask = legal_moves_mask(DummyState(n, moves))

    assert mask.sum() == 2
    for move in moves:
        assert mask[move_to_index(move, n)] == 1.0