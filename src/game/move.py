from typing import Literal
from pydantic.dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Move:
    orientation: Literal['H', 'V']
    row: int
    col: int
