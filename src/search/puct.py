import numpy as np
import numpy.typing as npt

from game import GameState
from search.node import Node


class PUCT:
    def __init__(self, action_size: int, c_puct: float = 1.5) -> None:
        self.action_size: int = action_size
        self.c_puct: float = c_puct
        self.root: Node | None = None

    def set_root(self, state: GameState) -> None:
        self.root = Node(state.clone(), action_size=self.action_size)

    def select(self, state: GameState) -> Node:
        if self.root is None:
            self.set_root(state)

        node = self.root

        while node.is_expanded and not node.state.is_terminal():
            action_index = node.select_action(self.c_puct)
            node = node.get_child(action_index)

        return node

    def expand(self, node: Node, policy: npt.NDArray[np.float32]) -> None:
        node.expand(policy)

    def backup(self, node: Node, value: float) -> None:
        node.backup(value)

    def get_policy(self, temperature: float = 1.0) -> npt.NDArray[np.float32]:
        """
        Convert visit counts to a probability distribution.
        temperature=0 returns a one-hot at the most-visited action (greedy).
        """
        visits = self.root.child_N.copy()

        if temperature == 0:
            policy = np.zeros_like(visits)
            policy[np.argmax(visits)] = 1.0
            return policy

        visits = visits ** (1.0 / temperature)
        total = visits.sum()
        if total > 0:
            visits /= total

        return visits

    def add_dirichlet_noise(self, epsilon: float = 0.25, alpha: float | None = None) -> None:
        """
        Mix Dirichlet noise into the root node's policy prior.
        Call this after expanding the root during training self-play.
        Not used during evaluation/inference.
        """
        if self.root is None or not self.root.is_expanded:
            return
        legal_indices = self.root.legal_indices
        if len(legal_indices) == 0:
            return
        if alpha is None:
            alpha = 10.0 / self.action_size
        noise = np.zeros(self.action_size, dtype=np.float32)
        noise[legal_indices] = np.random.dirichlet([alpha] * len(legal_indices))
        self.root.child_P = (1 - epsilon) * self.root.child_P + epsilon * noise

    def advance(self, action_index: int) -> None:
        """Move root to chosen child (tree reuse)."""
        if self.root and action_index in self.root.children:
            self.root = self.root.children[action_index]
            self.root.parent = None
        else:
            self.root = None
