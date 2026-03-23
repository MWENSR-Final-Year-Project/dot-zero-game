import numpy as np
from agents.base_agent import Agent
from analysis.move import creates_third_edge, boxes_completed_by
from game import GameState, Move


class DefensiveAgent(Agent):
    def __init__(self):
        super().__init__("Defensive")

    def select_move(self, state: GameState) -> Move:
        legal_moves = state.get_legal_moves()

        if not legal_moves:
            raise ValueError(
                "DefensiveAgent cannot select a move: No legal moves available"
            )

        move_scores = {move: boxes_completed_by(state, move) for move in legal_moves}
        best_move, best_score = max(move_scores.items(), key=lambda x: x[1])

        if best_score > 0:
            return best_move

        safe_moves = [
            move for move in legal_moves if not creates_third_edge(state, move)
        ]

        if safe_moves:
            return np.random.choice(safe_moves)

        return np.random.choice(legal_moves)
