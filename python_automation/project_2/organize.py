import argparse
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory


def organize(source, destination, apply):
    for item in sorted(source.iterdir()):
        if item.is_symlink() or not item.is_file():
            continue

        category = item.suffix.casefold().removeprefix(".") or "other"
        if category in {".", ".."}:
            category = "other"
        target = destination / category / item.name
        if target.exists():
            print(f"skip existing: {target}")
            continue
        if not apply:
            print(f"would copy: {item.name} -> {target}")
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=target.parent) as staging:
            temporary = Path(staging) / "copy"
            copyfile(item, temporary)
            try:
                target.hardlink_to(temporary)
            except FileExistsError:
                print(f"skip existing: {target}")
            else:
                print(f"copied: {target}")


def main():
    parser = argparse.ArgumentParser(description="Copy files into extension folders.")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    source = args.source.resolve()
    destination = args.destination.resolve()
    if not source.is_dir() or destination == source or destination.is_relative_to(source):
        parser.error("Choose an existing source folder and a separate destination.")
    try:
        organize(source, destination, args.apply)
    except OSError as error:
        parser.exit(1, f"Could not organize files: {error}\n")


if __name__ == "__main__":
    main()
