import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from src.iwlist import Cell


@dataclass
class Record:
    """Record keeping track of position and iwlist result"""

    x: float
    y: float
    cells: List[Cell]

    def dump(
        self, path: Optional[Path] = None, append: bool = True, delimiter: str = ","
    ) -> str:
        """Dumps to csv"""

        row = [str(self.x), str(self.y)]
        for cell in self.cells:
            row += [cell.essid, str(cell.signal_level)]

        if path is not None:
            with open(path, "a" if append else "w") as out:
                writer = csv.writer(out, delimiter=delimiter)
                writer.writerow(row)

        return delimiter.join(row)
