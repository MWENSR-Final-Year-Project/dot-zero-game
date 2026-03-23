from game import Board, Move


def get_adjacent_boxes(board: Board, move: Move):
    r, c = move.row, move.col
    offsets = [(-1, 0), (0, 0)] if move.orientation == "H" else [(0, -1), (0, 0)]

    for dr, dc in offsets:
        nr, nc = r + dr, c + dc
        if 0 <= nr < board.size and 0 <= nc < board.size:
            yield (nr, nc)
