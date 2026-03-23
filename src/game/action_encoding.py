import numpy as np

from game import Move, GameState


def move_to_index(move: Move, n: int) -> int:
    """
    Converts a Move to an integer index in [0, 2*n*(n+1) - 1].
    Horizontal moves first, then vertical moves.
    """
    if move.orientation == "H":
        # Horizontal edges: row in [0, n], col in [0, n-1]
        return move.row * n + move.col
    elif move.orientation == "V":
        # Vertical edges: row in [0, n-1], col in [0, n]
        offset = (n + 1) * n
        return offset + move.row * (n + 1) + move.col
    else:
        raise ValueError(f"Invalid move orientation: {move.orientation}")


def index_to_move(index: int, n: int) -> Move:
    """
    Converts an index back to a Move object.
    """
    horizontal_count = (n + 1) * n

    if index < horizontal_count:
        row = index // n
        col = index % n
        return Move("H", row, col)
    else:
        index -= horizontal_count
        row = index // (n + 1)
        col = index % (n + 1)
        return Move("V", row, col)


def legal_moves_mask(state: GameState) -> np.ndarray:
    """
    Returns a flat mask of legal moves for neural network policy.
    1 = legal, 0 = illegal
    """
    n = state.board.size
    total_actions = num_actions(n)
    mask = np.zeros(total_actions, dtype=np.float32)

    for move in state.get_legal_moves():
        idx = move_to_index(move, n)
        mask[idx] = 1.0

    return mask


def num_actions(n: int) -> int:
    """
    Returns total number of possible moves for an n x n board.
    """
    return 2 * n * (n + 1)
