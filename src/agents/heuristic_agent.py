import numpy as np
from agents.base_agent import Agent
from analysis.move import (
    boxes_completed_by,
    boxes_given_to_opponent,
    creates_third_edge,
)
from game import GameState, Move


class HeuristicAgent(Agent):
    def __init__(self):
        super().__init__("Heuristic")

    def select_move(self, state: GameState) -> Move:
        legal_moves = state.get_legal_moves()

        if not legal_moves:
            raise ValueError(
                "HeuristicAgent cannot select a move: No legal moves available"
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

        return min(legal_moves, key=lambda move: boxes_given_to_opponent(state, move))
