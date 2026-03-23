from copy import deepcopy
from typing import Counter, List

from game.board import Board
from game.move import  Move


class GameState:
    def __init__(self, board: Board, current_player: int = -1) -> None:
        self.board = board
        self.current_player = current_player
        self.scores = Counter({-1: 0, 1: 0})

    def clone(self) -> "GameState":
        return deepcopy(self)

    def get_legal_moves(self) -> List[Move]:
        moves = []

        for r in range(self.board.size + 1):
            for c in range(self.board.size):
                move = Move("H", r, c)
                if not self.board.is_edge_filled(move):
                    moves.append(move)

        for r in range(self.board.size):
            for c in range(self.board.size + 1):
                move = Move("V", r, c)
                if not self.board.is_edge_filled(move):
                    moves.append(move)

        return moves

    def apply_move(self, move: Move) -> "GameState":
        new_state = self.clone()
        board = new_state.board
        player = new_state.current_player

        board.add_edge(move)
        completed_boxes = board.get_completed_boxes(move)

        if completed_boxes:
            for r, c in completed_boxes:
                board.boxes[r, c] = player
                new_state.scores[player] += 1
        else:
            new_state.current_player *= -1

        return new_state

    def is_terminal(self) -> bool:
        return len(self.get_legal_moves()) == 0

    def get_winner(self) -> int:
        if self.scores[1] > self.scores[-1]:
            return 1

        if self.scores[-1] > self.scores[1]:
            return -1

        return 0
