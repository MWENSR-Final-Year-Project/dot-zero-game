from abc import ABC, abstractmethod
from typing import List, Tuple
from analysis.move import boxes_completed_by, creates_third_edge
from game import GameState, Move


class Agent(ABC):
    def __init__(self, name: str):
        self.name = name

    def select_move(self, state: GameState) -> Move:
        legal_moves = self._require_legal_moves(state)
        best_move, best_score = self._best_scoring_move(state, legal_moves)
        if best_score > 0:
            return best_move
        safe_moves = self._safe_moves(state, legal_moves)
        return self._fallback(state, legal_moves, safe_moves)

    @abstractmethod
    def _fallback(self, state: GameState, legal_moves: List[Move], safe_moves: List[Move]) -> Move:
        pass

    def _require_legal_moves(self, state: GameState) -> List[Move]:
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            raise ValueError(f"{self.name} cannot select a move: No legal moves available")
        return legal_moves

    def _best_scoring_move(self, state: GameState, legal_moves: List[Move]) -> Tuple[Move, int]:
        move_scores = {move: boxes_completed_by(state, move) for move in legal_moves}
        return max(move_scores.items(), key=lambda x: x[1])

    def _safe_moves(self, state: GameState, legal_moves: List[Move]) -> List[Move]:
        return [m for m in legal_moves if not creates_third_edge(state, m)]
