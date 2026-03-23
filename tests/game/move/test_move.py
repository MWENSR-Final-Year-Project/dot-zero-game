from dataclasses import FrozenInstanceError
import pytest
from pydantic import ValidationError
from game import Move

def test_move_creation_valid():
    m = Move('H', 1, 2)
    assert m.orientation == 'H'
    assert m.row == 1
    assert m.col == 2

def test_move_invalid_orientation_raises():
    with pytest.raises(ValidationError):
        Move('Q', 0, 0)

def test_move_is_immutable():
    m = Move('V', 0, 1)
    with pytest.raises(FrozenInstanceError):
        m.row = 3

def test_move_equality():
    m1 = Move('H', 1, 2)
    m2 = Move('H', 1, 2)
    m3 = Move('V', 1, 2)

    assert m1 == m2
    assert m1 != m3

def test_move_is_hashable():
    m1 = Move('H', 0, 1)
    m2 = Move('H', 0, 1)

    move_set = {m1}
    assert m2 in move_set
