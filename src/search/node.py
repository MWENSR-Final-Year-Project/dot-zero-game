from __future__ import annotations

from typing import Dict, Optional

import numpy as np
import numpy.typing as npt

from game import GameState, index_to_move, move_to_index, state_to_tensor


class Node:
    def __init__(
        self,
        state: GameState,
        parent: Optional[Node] = None,
        action_taken: Optional[int] = None,
        action_size: int = 0,
    ) -> None:
        self.state: GameState = state
        self.parent: Optional[Node] = parent
        self.action_taken: Optional[int] = action_taken
        self.action_size: int = action_size

        self.tensor: npt.NDArray[np.float32] = state_to_tensor(state)
        self.hash: int = hash(state)

        self.children: Dict[int, Node] = {}

        self.child_N: npt.NDArray[np.float32] = np.zeros(action_size, dtype=np.float32)
        self.child_W: npt.NDArray[np.float32] = np.zeros(action_size, dtype=np.float32)
        self.child_P: npt.NDArray[np.float32] = np.zeros(action_size, dtype=np.float32)

        self.total_N: float = 0.0

        legal_moves = state.get_legal_moves()
        self.legal_indices: npt.NDArray[np.int32] = np.array(
            [move_to_index(m, state.board.size) for m in legal_moves],
            dtype=np.int32,
        )

        self.legal_mask: npt.NDArray[np.float32] = np.zeros(action_size, dtype=np.float32)
        self.legal_mask[self.legal_indices] = 1.0

        self.is_expanded: bool = False

    def child_Q(self) -> npt.NDArray[np.float32]:
        return self.child_W / (1.0 + self.child_N)

    def child_U(self, c_puct: float) -> npt.NDArray[np.float32]:
        return (
            c_puct * self.child_P * np.sqrt(self.total_N + 1e-8) / (1.0 + self.child_N)
        )

    def select_action(self, c_puct: float) -> int:
        scores = self.child_Q() + self.child_U(c_puct)
        scores = scores * self.legal_mask - (1 - self.legal_mask) * 1e9
        return int(np.argmax(scores))

    def expand(self, policy: npt.NDArray[np.float32]) -> None:
        self.is_expanded = True

        if len(self.legal_indices) == 0:
            return

        policy = policy * self.legal_mask
        policy_sum = policy.sum()

        if policy_sum > 0:
            policy /= policy_sum
        else:
            policy[self.legal_indices] = 1.0 / len(self.legal_indices)

        self.child_P = policy

    def get_child(self, action_index: int) -> Node:
        if action_index not in self.children:
            move = index_to_move(action_index, self.state.board.size)
            next_state = self.state.clone().apply_move(move)
            self.children[action_index] = Node(
                next_state,
                parent=self,
                action_taken=action_index,
                action_size=self.action_size,
            )
        return self.children[action_index]

    def backup(self, value: float) -> None:
        node = self
        while node.parent is not None:
            parent = node.parent
            if parent.state.current_player != node.state.current_player:
                value = -value
            parent.child_N[node.action_taken] += 1
            parent.child_W[node.action_taken] += value
            parent.total_N += 1
            node = parent
