from typing import Any, List, Optional, Protocol, Tuple

import numpy as np
import numpy.typing as npt
import torch

from agents.base_agent import Agent
from game import GameState, Move, index_to_move, num_actions
from search.puct import PUCT


class NeuralNet(Protocol):

    def eval(self) -> None: ...

    def __call__(self, x: Any) -> Tuple[Any, Any]: ...


class NGMCTSAgent(Agent):
    def __init__(
        self,
        model: NeuralNet,
        device: Optional[torch.device],
        board_size: int,
        c_puct: float = 1.5,
        num_simulations: int = 100,
        temperature: float = 0.1,
    ) -> None:
        super().__init__("ng_mcts")
        self.model: NeuralNet = model
        self.device: Optional[torch.device] = device
        self.board_size: int = board_size
        self.action_size: int = num_actions(board_size)
        self.c_puct: float = c_puct
        self.num_simulations: int = num_simulations
        self.temperature: float = temperature

    def select_move(self, state: GameState) -> Move:
        self._require_legal_moves(state)

        self.model.eval()

        tree = PUCT(self.action_size, self.c_puct)

        for _ in range(self.num_simulations):
            leaf = tree.select(state)
            if leaf.state.is_terminal():
                tree.backup(leaf, 0.0)
                continue
            with torch.inference_mode():
                tensor = torch.from_numpy(leaf.tensor).permute(2, 0, 1).unsqueeze(0).to(self.device)
                policy_logits, value = self.model(tensor)
                policy_np: npt.NDArray[np.float32] = (
                    torch.softmax(policy_logits, dim=1)[0].cpu().numpy()
                )
            tree.expand(leaf, policy_np)
            tree.backup(leaf, float(value[0].item()))

        policy: npt.NDArray[np.float32] = tree.get_policy(temperature=self.temperature)
        move_index: int = int(np.argmax(policy))
        return index_to_move(move_index, self.board_size)

    def _fallback(self, state: GameState, legal_moves: List[Move], safe_moves: List[Move]) -> Move:
        pass
