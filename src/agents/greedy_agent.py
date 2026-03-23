from typing import List

import numpy as np
from agents.base_agent import Agent
from analysis.move.boxes_completed_by_move import boxes_completed_by
from game import GameState, Move


class GreedyAgent(Agent):

    def __init__(self):
        super().__init__("Greedy")

    def select_move(self, state: GameState) -> Move:
        legal_moves = state.get_legal_moves()

        if not legal_moves:
            raise ValueError(
                "GreedyAgent cannot select a move: No legal moves available"
            )

        best_move = max(legal_moves, key=lambda move: boxes_completed_by(state, move))

        if boxes_completed_by(state, best_move) > 0:
            return best_move

        return np.random.choice(legal_moves)

    def _fallback(self, state: GameState, legal_moves: List[Move], safe_moves: List[Move]) -> Move:
        pass
