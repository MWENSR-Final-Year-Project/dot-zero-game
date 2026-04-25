from typing import List
import numpy as np
from agents.base_agent import Agent
from game import GameState, Move


class RandomAgent(Agent):

    def __init__(self):
        super().__init__("random")

    def select_move(self, state: GameState) -> Move:
        legal_moves = state.get_legal_moves()

        if not legal_moves:
            raise ValueError(
                "RandomAgent cannot select a move: No legal moves available"
            )

        return np.random.choice(legal_moves)

    def _fallback(self, state: GameState, legal_moves: List[Move], safe_moves: List[Move]) -> Move:
        pass
