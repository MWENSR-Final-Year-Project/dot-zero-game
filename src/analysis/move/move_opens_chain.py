from game import GameState, Move


def opens_chain(state: GameState, move: Move) -> bool:
    new_state = state.clone()
    new_state.board.add_edge(move)

    for r in range(new_state.board.size):
        for c in range(new_state.board.size):
            if _edge_count(new_state, r, c) == 2:
                if _has_two_edge_neighbour(new_state, r, c):
                    return True
    return False


def _edge_count(state: GameState, r: int, c: int) -> int:
    b = state.board
    return (
        int(b.horizontal_edges[r, c])
        + int(b.horizontal_edges[r + 1, c])
        + int(b.vertical_edges[r, c])
        + int(b.vertical_edges[r, c + 1])
    )


def _has_two_edge_neighbour(state: GameState, r: int, c: int) -> bool:
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < state.board.size and 0 <= nc < state.board.size:
            if _edge_count(state, nr, nc) == 2:
                return True
    return False
