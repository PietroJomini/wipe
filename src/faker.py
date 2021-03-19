from dataclasses import dataclass
from math import sqrt
from random import random
from typing import List, Tuple

from src.iwlist import Cell
from src.record import Record


@dataclass
class FakeCell:
    """Fake cel builder"""

    name: str
    x: float
    y: float

    def __init__(self, name: str, max_x: float = 100, max_y: float = 100):
        self.x = random() * max_x
        self.y = random() * max_y
        self.name = name

    def at(self, x: float, y: float):
        """Create new Cell with `signal_level` equal to the distance from the target"""

        dx = self.x - x
        dy = self.y - y
        signal_level = sqrt(dx ** 2 + dy ** 2)
        return Cell(self.name, signal_level)


def fake_data(
    n_cells: int,
    n_measures: int,
    max_x: float = 100,
    max_y: float = 100,
) -> Tuple[List[FakeCell], List[Record]]:
    """Generate random fake data"""

    cells = [FakeCell(f"cell_{i}", max_x=max_x, max_y=max_y) for i in range(n_cells)]
    positions = [(random() * max_y, random() * max_y) for _ in range(n_measures)]
    measures = [Record(x, y, [cell.at(x, y) for cell in cells]) for x, y in positions]

    return cells, measures
