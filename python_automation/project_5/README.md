# Project 5 — ZIP backup

**Build** Create a ZIP backup with a SHA-256 manifest for every archived file.

```sh
mkdir -p output
python3 project_5/backup.py project_1/sample output/inventory-backup.zip
python3 -m zipfile -l output/inventory-backup.zip
python3 -m zipfile -t output/inventory-backup.zip
```

Expect two files under `files/` in the archive, plus `manifest.json`. The final command checks the ZIP's built-in integrity information.

## How it works

1. [backup.py](backup.py) uses `rglob("*")` to visit nested files and `relative_to` to keep only their paths inside the input folder.
2. `ZipFile.write` streams each file into the archive. The second pass computes the SHA-256 hashes from the archived bytes themselves. The manifest associates each path with its hash.
3. The staged ZIP is published under the requested filename only after both passes succeed. Publication uses a hard link on the destination filesystem. Reusing a destination name fails with the original archive intact.
4. The sample archives file contents. Empty directories are skipped. For changing input files, back up a stable copy if the files need to represent one point in time.

## Your turn

- Choose another output name and back up a folder with a nested file. Check that the relative path appears in the archive.
- Run the same command twice with the same output name. Check the second run fails and the first ZIP is still readable.
- Write a verifier that opens the manifest, opens each listed member by name, and compares its checksum. Test with an archive where you deliberately alter a manifest digest.

[Next — Daily sales pipeline](../project_6/README.md)
