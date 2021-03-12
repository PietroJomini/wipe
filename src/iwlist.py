import re
import subprocess
from dataclasses import dataclass
from typing import List, Union


class ParseError(Exception):
    """Raised on generic parse error"""


@dataclass
class Cell:
    """Cell meta"""

    essid: str
    signal_level: int


class Scanner:
    """Call `iwlist scan` and parse the signal levels of the found cells"""

    def __init__(self, interface: str):
        self.interface = interface

    def call(
        self,
        use_sudo: Union[bool, str] = True,
        sudo_cmd="sudo",
        iwlist_cmd="iwlist",
        scan_cmd="scan",
    ) -> subprocess.CompletedProcess:
        """Call `iwlist scan` on the given interface"""

        cmd = [iwlist_cmd, self.interface, scan_cmd]

        if use_sudo is not False:
            sudo = use_sudo if type(use_sudo) is str else sudo_cmd
            cmd = [sudo] + cmd

        return subprocess.run(cmd, capture_output=True)

    def parse(
        self,
        stdout: Union[str, subprocess.CompletedProcess],
        cell_pattern: str = r"Cell (\d{2}).*",
        essid_pattern: str = r'ESSID:"(.*)"',
        signal_level_pattern: str = r"Quality=(?:\d{2}\/\d{2})  Signal level=(-?\d+).*",
    ) -> List[Cell]:
        """Parse `iwlist scan` result"""

        if isinstance(stdout, subprocess.CompletedProcess):
            stdout = stdout.stdout.decode()

        res = []
        essid = None
        signal_level = None

        for index, line in enumerate(stdout.splitlines()):
            line = line.strip()

            if re.match(essid_pattern, line):
                essid = re.search(essid_pattern, line).group(1)

            if re.match(signal_level_pattern, line):
                signal_level = re.search(signal_level_pattern, line).group(1)
                signal_level = int(signal_level)

            if (
                re.match(cell_pattern, line)
                and essid is not None
                and signal_level is not None
            ):
                res.append(Cell(essid, signal_level))
                essid = None
                signal_level = None

        if essid is not None and signal_level is not None:
            res.append(Cell(essid, signal_level))
            essid = None
            signal_level = None

        return res
