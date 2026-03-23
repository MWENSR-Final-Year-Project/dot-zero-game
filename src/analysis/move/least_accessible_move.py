from game import GameState, Move
from analysis.move.move_creates_third_edge import creates_third_edge


def opponent_accessible_boxes(state: GameState, move: Move) -> int:
    new_state = state.apply_move(move)
    return sum(
        1 for m in new_state.get_legal_moves()
        if creates_third_edge(new_state, m)
    )