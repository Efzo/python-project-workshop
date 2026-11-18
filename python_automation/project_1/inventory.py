import argparse
from collections import Counter
from pathlib import Path


def inventory(folder):
    counts = Counter()
    for path in folder.iterdir():
        if path.is_file() and not path.is_symlink():
            extension = path.suffix.casefold() or "(no extension)"
            counts[extension] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description="Count files by extension.")
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    try:
        counts = inventory(args.folder)
    except OSError as error:
        parser.exit(1, f"Could not read folder: {error}\n")
    for extension, count in sorted(counts.items()):
        print(f"{extension}: {count}")
    print(f"Total: {sum(counts.values())}")


if __name__ == "__main__":
    main()
