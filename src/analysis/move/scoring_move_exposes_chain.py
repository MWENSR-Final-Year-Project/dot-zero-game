from game import GameState, Move
from analysis.move.boxes_completed_by_move import boxes_completed_by
from analysis.move.move_opens_chain import opens_chain


def scoring_move_exposes_chain(state: GameState, move: Move) -> bool:
    if boxes_completed_by(state, move) == 0:
        return False
    new_state = state.apply_move(move)
    return any(
        opens_chain(new_state, m)
        for m in new_state.get_legal_moves()
    )
