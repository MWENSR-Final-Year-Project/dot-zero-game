from game import Board, GameState, Move

def _state_with_three_sides(col=0):
    state = GameState(Board(size=3))
    board = state.board
    board.horizontal_edges[0, col] = 1
    board.vertical_edges[0, col] = 1
    board.vertical_edges[0, col + 1] = 1
    return state


def test_apply_move_completes_box_and_updates_score():
    state = _state_with_three_sides(col=0)
    new_state = state.apply_move(Move("H", 1, 0))

    assert new_state.board.boxes[0, 0] == -1
    assert new_state.scores[-1] == 1


def test_apply_move_completes_two_boxes():
    state = GameState(Board(size=3))
    board = state.board

    board.horizontal_edges[0, 1] = 1
    board.vertical_edges[0, 1] = 1
    board.vertical_edges[0, 2] = 1
    board.horizontal_edges[2, 1] = 1
    board.vertical_edges[1, 1] = 1
    board.vertical_edges[1, 2] = 1

    new_state = state.apply_move(Move("H", 1, 1))

    assert new_state.scores[-1] == 2