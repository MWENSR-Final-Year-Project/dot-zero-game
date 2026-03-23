from game import Board, GameState


def test_clone_returns_new_instance():
    state = GameState(Board(size=3))
    assert state.clone() is not state


def test_clone_board_is_independent():
    state = GameState(Board(size=3))
    assert state.clone().board is not state.board