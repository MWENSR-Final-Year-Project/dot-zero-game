import numpy as np
from agents.base_agent import Agent
from analysis.move import boxes_given_to_opponent, opponent_accessible_boxes
from game import GameState, Move

class HeuristicAgent(Agent):
    def __init__(self):
        super().__init__("Heuristic")

    def _fallback(self, state: GameState, legal_moves, safe_moves) -> Move:
        candidates = safe_moves if safe_moves else legal_moves
        return min(candidates, key=lambda m: opponent_accessible_boxes(state, m))