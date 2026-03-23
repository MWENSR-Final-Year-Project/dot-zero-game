from game import Board, GameState,  Move


def test_initial_board_has_all_edges_legal():
    board = Board(size=3)
    state = GameState(board)

    horizontal = (board.size + 1) * board.size
    vertical = board.size * (board.size + 1)

    assert len(state.get_legal_moves()) == horizontal + vertical


def test_marked_edge_not_in_legal_moves():
    board = Board(size=3)
    state = GameState(board)
    move = Move("H", 0, 0)

    legal_moves = state.get_legal_moves()
    state.board.horizontal_edges[0][0] = 1
    new_legal_moves = state.get_legal_moves()

    assert move not in new_legal_moves
    assert len(new_legal_moves) == len(legal_moves) - 1
