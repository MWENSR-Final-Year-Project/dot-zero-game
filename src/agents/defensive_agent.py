import numpy as np
from agents.base_agent import Agent
from analysis.move import opens_chain, scoring_move_exposes_chain
from game import GameState, Move


class DefensiveAgent(Agent):
    def __init__(self):
        super().__init__("Defensive")

    def select_move(self, state: GameState) -> Move:
        legal_moves = self._require_legal_moves(state)
        best_move, best_score = self._best_scoring_move(state, legal_moves)

        if best_score > 0 and not scoring_move_exposes_chain(state, best_move):
            return best_move

        safe_moves = [
            m for m in self._safe_moves(state, legal_moves)
            if not opens_chain(state, m)
        ]

        return self._fallback(state, legal_moves, safe_moves)

    def _fallback(self, state: GameState, legal_moves, safe_moves) -> Move:
        if safe_moves:
            return np.random.choice(safe_moves)
        return np.random.choice(legal_moves)