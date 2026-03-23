from analysis.move import boxes_completed_by
from game import GameState, Move


def boxes_given_to_opponent(state: GameState, move: Move) -> int:
    new_state = state.apply_move(move)

    total = 0

    while True:
        legal_moves = new_state.get_legal_moves()
        if not legal_moves:
            break

        move_scores = {m: boxes_completed_by(new_state, m) for m in legal_moves}

        best_move, best_score = max(move_scores.items(), key=lambda x: x[1])

        if best_score == 0:
            break

        total += best_score
        new_state = new_state.apply_move(best_move)

    return total
