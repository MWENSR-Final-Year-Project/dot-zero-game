from game import Board, GameState,  Move

def test_turn_switches_when_no_box_completed():
    state = GameState(Board(size=3))
    new_state = state.apply_move(Move("H", 0, 0))

    assert new_state.current_player == -state.current_player


def test_turn_does_not_switch_when_box_completed():
    state = GameState(Board(size=3))
    board = state.board
    board.horizontal_edges[0, 0] = 1
    board.vertical_edges[0, 0] = 1
    board.vertical_edges[0, 1] = 1

    new_state = state.apply_move(Move("H", 1, 0))

    assert new_state.current_player == state.current_player
