from game.analysis.box import get_adjacent_boxes, count_edges_around_box
from game.move import Move
from game.state import GameState


def creates_third_edge(state: GameState, move: Move) -> bool:
    board = state.board
    boxes = get_adjacent_boxes(board, move)

    for r, c in boxes:
        if count_edges_around_box(board, r, c) == 2:
            return True

    return False
