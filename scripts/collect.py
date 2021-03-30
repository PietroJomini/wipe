from sys import argv
from typing import Dict, List

from src.iwlist import Cell, Scanner


def update_ds(ds: Dict[str, List[float]], cells: List[Cell]) -> Dict[str, List[float]]:

    # adding new data
    records = max([len(ds[mac]) for mac in ds]) - 1
    for cell in cells:
        if cell.mac not in ds:
            ds[cell.mac] = ["-"] * records
        ds[cell.mac].append(cell.signal_level)

    # filling missing data
    records += 1
    for mac in ds:
        if len(ds[mac]) != records:
            ds[mac] += ["-"] * (records - len(ds[mac]))

    return ds


def ds2csv(ds: Dict[str, List[float]]) -> List[str]:

    csv = [list(ds)]

    for i in range(len(ds["label"])):
        row = [str(ds[key][i]) for key in ds if i < len(ds[key])]
        csv.append(row)

    return [",".join(row) for row in csv]


def cli(out: str):

    scanner = Scanner("wlo1")
    ds = {"label": []}
    label = ""

    while True:
        token = input("wipe > ")
        token = token.lower()
        tokens = token.split(" ")

        if tokens[0] == "exit":
            break

        elif tokens[0] == "":
            if label == "":
                print("wipe | label is not set")
                continue

            print("wipe | scanning")
            cells = scanner.parse(scanner.call())

            print("wipe | updating dataset")
            ds["label"].append(label)
            ds = update_ds(ds, cells)

            print(f"wipe | found {len(cells)} cells")
            print(f"wipe | writing data to {out}")

            with open(out, "w") as ds_file:
                ds_file.write("\n".join(ds2csv(ds)))

        elif tokens[0] == "label":
            if len(tokens) < 2:
                print(
                    f"wipe | current label = {label}"
                    if label != ""
                    else "wipe | label is not set"
                )
            else:
                label = tokens[1]
                print(f"wipe | label set to {label}")


if __name__ == "__main__":
    cli(argv[1])
