import numpy as np

from game.move import Move
from game.state import GameState


def move_to_index(move: Move, n: int) -> int:
    if move.orientation == "H":
        return move.row * n + move.col

    if move.orientation == "V":
        offset = (n + 1) * n
        return offset + move.row * (n + 1) + move.col

    raise ValueError(f"Invalid move orientation: {move.orientation}")


def index_to_move(index: int, n: int) -> Move:
    horizontal_count = (n + 1) * n

    if index < horizontal_count:
        row = index // n
        col = index % n
        return Move("H", row, col)

    index -= horizontal_count
    row = index // (n + 1)
    col = index % (n + 1)
    return Move("V", row, col)


def legal_moves_mask(state: GameState) -> np.ndarray:
    n = state.board.size
    total_actions = num_actions(n)
    mask = np.zeros(total_actions, dtype=np.float32)

    for move in state.get_legal_moves():
        idx = move_to_index(move, n)
        mask[idx] = 1.0

    return mask


def num_actions(n: int) -> int:
    return 2 * n * (n + 1)
