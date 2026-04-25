"""
State-to-array encoding for neural network input.

Encodes a GameState as a float32 numpy array of shape (H, W, C)
where H = W = n+1 and C = 4 (horizontal edges, vertical edges,
current player's boxes, opponent's boxes).
"""

import numpy as np
import numpy.typing as npt

from game.state import GameState


def state_to_tensor(state: GameState) -> npt.NDArray[np.float32]:
    """
    Encode `state` as a float32 array of shape (n+1, n+1, 4).

    Channels:
        0 — horizontal edges
        1 — vertical edges
        2 — current player's boxes
        3 — opponent's boxes
    """
    board = state.board
    n = board.size

    H = W = n + 1
    C = 4

    out = np.zeros((H, W, C), dtype=np.float32)

    out[:, :n, 0] = board.horizontal_edges.astype(np.float32)
    out[:n, :, 1] = board.vertical_edges.astype(np.float32)

    boxes = board.boxes

    if state.current_player == 1:
        out[:n, :n, 2] = (boxes == 1).astype(np.float32)
        out[:n, :n, 3] = (boxes == -1).astype(np.float32)
    else:
        out[:n, :n, 2] = (boxes == -1).astype(np.float32)
        out[:n, :n, 3] = (boxes == 1).astype(np.float32)

    return out
