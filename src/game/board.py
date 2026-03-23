from typing import List
import numpy as np
from game.move import Move


class Board:
    def __init__(self, size: int) -> None:
        self.size = size
        self.horizontal_edges = np.zeros((size + 1, size), dtype=np.int8)
        self.vertical_edges = np.zeros((size, size + 1), dtype=np.int8)
        self.boxes = np.zeros((size, size), dtype=np.int8)

    def is_edge_filled(self, move: Move) -> bool:
        if move.orientation == "H":
            return self.horizontal_edges[move.row][move.col] == 1

        return self.vertical_edges[move.row][move.col] == 1

    def is_box_completed(self, r: int, c: int) -> bool:
        return (
            1
            == self.horizontal_edges[r, c]
            == self.horizontal_edges[r + 1, c]
            == self.vertical_edges[r, c]
            == self.vertical_edges[r, c + 1]
        )

    def get_completed_boxes(self, move: Move) -> List[tuple]:
        completed = []

        if move.orientation == "H":
            r, c = move.row, move.col

            if r > 0 and self.is_box_completed(r - 1, c):
                completed.append((r - 1, c))
            if r < self.size and self.is_box_completed(r, c):
                completed.append((r, c))

        else:
            r, c = move.row, move.col

            if c > 0 and self.is_box_completed(r, c - 1):
                completed.append((r, c - 1))
            if c < self.size and self.is_box_completed(r, c):
                completed.append((r, c))

        return completed

    def add_edge(self, move: Move):
        if self.is_edge_filled(move):
            raise ValueError("Edge already filled")
        if move.orientation == "H":
            self.horizontal_edges[move.row, move.col] = 1
        else:
            self.vertical_edges[move.row, move.col] = 1
