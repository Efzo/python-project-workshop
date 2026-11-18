import argparse
from hashlib import file_digest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile


def create_backup(source, destination):
    files = sorted(path for path in source.rglob("*") if path.is_file() and not path.is_symlink())
    with TemporaryDirectory(dir=destination.parent) as staging:
        temporary = Path(staging) / "backup.zip"
        with ZipFile(temporary, "w", compression=ZIP_DEFLATED) as archive:
            for path in files:
                relative = path.relative_to(source).as_posix()
                archive.write(path, f"files/{relative}")
        with ZipFile(temporary) as archive:
            manifest = {}
            for name in archive.namelist():
                with archive.open(name) as contents:
                    manifest[name] = file_digest(contents, "sha256").hexdigest()
        with ZipFile(temporary, "a") as archive:
            archive.writestr("manifest.json", json.dumps(manifest, indent=2))
        destination.hardlink_to(temporary)
    return len(files)


def main():
    parser = argparse.ArgumentParser(description="Create a ZIP backup with a checksum manifest.")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    source = args.source.resolve()
    destination = args.destination.absolute()
    if not source.is_dir() or destination.parent.resolve().is_relative_to(source):
        parser.error("Use an existing source and an output path outside it.")
    try:
        count = create_backup(source, destination)
    except OSError as error:
        parser.exit(1, f"Could not create backup: {error}\n")
    print(f"Archived {count} file(s) to {destination}")


if __name__ == "__main__":
    main()
