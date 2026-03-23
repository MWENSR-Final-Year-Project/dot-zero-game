from abc import ABC, abstractmethod
from game import GameState, Move


class Agent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def select_move(self, state: GameState) -> Move:
        pass
