from game import Board, GameState, Move

def test_apply_move_returns_new_state():
    state = GameState(Board(size=3))
    new_state = state.apply_move(Move("H", 0, 0))

    assert new_state is not state
    assert new_state.board is not state.board


def test_apply_move_does_not_mutate_original():
    state = GameState(Board(size=3))
    new_state = state.apply_move(Move("V", 1, 1))

    assert state.board.vertical_edges.sum() == 0
    assert new_state.board.vertical_edges.sum() == 1


def test_apply_move_adds_edge():
    state = GameState(Board(size=3))
    new_state = state.apply_move(Move("H", 2, 1))

    assert new_state.board.horizontal_edges[2, 1] == 1


def test_apply_move_no_completed_boxes():
    state = GameState(Board(size=3))
    new_state = state.apply_move(Move("H", 0, 1))

    assert new_state.scores == state.scores
    assert (new_state.board.boxes == state.board.boxes).all()
