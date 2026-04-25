import random
from typing import List

import numpy as np

from agents.base_agent import Agent
from game import GameState, Move, index_to_move, num_actions
from search.puct import PUCT


class MCTSAgent(Agent):
    def __init__(self, num_simulations: int = 100, c_puct: float = 1.41) -> None:
        super().__init__("pure_mcts")
        self.num_simulations = num_simulations
        self.c_puct = c_puct

    def select_move(self, state: GameState) -> Move:
        self._require_legal_moves(state)
        if state.is_terminal():
            raise ValueError("select_move called on terminal state")

        action_size = num_actions(state.board.size)
        tree = PUCT(action_size, self.c_puct)

        for _ in range(self.num_simulations):
            leaf = tree.select(state)
            value = self._rollout(leaf.state)
            if not leaf.is_expanded and not leaf.state.is_terminal():
                uniform: np.ndarray = np.zeros(action_size, dtype=np.float32)
                uniform[leaf.legal_indices] = 1.0 / len(leaf.legal_indices)
                tree.expand(leaf, uniform)
            tree.backup(leaf, value)

        policy = tree.get_policy(temperature=0)
        return index_to_move(int(np.argmax(policy)), state.board.size)

    def _fallback(self, state: GameState, legal_moves: List[Move], safe_moves: List[Move]) -> Move:
        pass

    def _rollout(self, state: GameState) -> float:
        rollout_player = state.current_player
        while not state.is_terminal():
            state = state.apply_move(random.choice(state.get_legal_moves()))
        winner = state.get_winner()
        if winner == rollout_player:
            return 1.0
        if winner == 0:
            return 0.0
        return -1.0
