import re
import subprocess
from dataclasses import dataclass
from typing import List, Union


@dataclass
class Cell:
    """Cell meta"""

    essid: str
    mac: str
    signal_level: float


class Scanner:
    """Call `iwlist scan` and parse the signal levels of the found cells"""

    def __init__(self, interface: str):
        self.interface = interface

    def call(
        self,
        use_sudo: Union[bool, str] = True,
        sudo_cmd: str = "sudo",
        iwlist_cmd: str = "iwlist",
        scan_cmd: str = "scan",
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
        mac_pattern: str = r"Cell (?:\d+) - Address: (.+)",
        signal_level_pattern: str = r"Quality=(?:\d{2}\/\d{2})  Signal level=(-?\d+).*",
    ) -> List[Cell]:
        """Parse `iwlist scan` result"""

        if isinstance(stdout, subprocess.CompletedProcess):
            stdout = stdout.stdout.decode()

        res = []
        essid = None
        signal_level = None
        mac = None

        for index, line in enumerate(stdout.splitlines()):
            line = line.strip()

            if (
                re.match(cell_pattern, line)
                and mac is not None
                and essid is not None
                and signal_level is not None
            ):
                res.append(Cell(essid=essid, mac=mac, signal_level=signal_level))
                signal_level = None
                essid = None
                mac = None

            if re.match(essid_pattern, line):
                essid = re.search(essid_pattern, line).group(1)

            if re.match(mac_pattern, line):
                mac = re.search(mac_pattern, line).group(1)

            if re.match(signal_level_pattern, line):
                signal_level = re.search(signal_level_pattern, line).group(1)
                signal_level = signal_level

        if essid is not None and mac is not None and signal_level is not None:
            res.append(Cell(essid=essid, mac=mac, signal_level=signal_level))
            signal_level = None
            essid = None
            mac = None

        return res
