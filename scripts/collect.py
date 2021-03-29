from sys import argv

from src.iwlist import Scanner
from src.record import Record


def cli(out: str):

    scanner = Scanner("wlo1")
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

            print(f"wipe | found {len(cells)} cells")
            print(f"wipe | writing data to {out}")

            record = Record(label, cells)
            with open(out, "a") as data:
                data.writelines(f"\n{record.dump()}")

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
