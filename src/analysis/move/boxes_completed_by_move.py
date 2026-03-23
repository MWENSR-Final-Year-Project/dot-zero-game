from game import GameState, Move


def boxes_completed_by(state: GameState, move: Move) -> int:
    current_player = state.current_player
    current_score = state.scores[current_player]

    new_state = state.apply_move(move)
    new_score = new_state.scores[current_player]

    return new_score - current_score
