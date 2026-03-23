from game.board import Board
from game.move import Move


def count_edges_around_box(board: Board, r: int, c: int) -> int:
    edges = (
        Move("H", r, c),
        Move("H", r + 1, c),
        Move("V", r, c),
        Move("V", r, c + 1),
    )

    return sum(board.is_edge_filled(edge) for edge in edges)
