import csv
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


PROJECT_DIRECTORY = Path(__file__).resolve().parent


class TaskboardTests(unittest.TestCase):
    def setUp(self):
        temporary = self.enterContext(TemporaryDirectory())
        self.directory = Path(temporary)
        self.database = self.directory / "test.db"

    def run_board(self, *arguments, check=True):
        return subprocess.run(
            [sys.executable, "-m", "taskboard", "--db", str(self.database), *arguments],
            cwd=PROJECT_DIRECTORY,
            capture_output=True,
            text=True,
            check=check,
        )

    def test_task_lifecycle_and_csv_export(self):
        self.run_board("add", "Read, then revise", "--due", "2026-12-15")
        self.assertIn("(due 2026-12-15)", self.run_board("list").stdout)
        self.run_board("done", "1")
        self.assertEqual(self.run_board("list").stdout.strip(), "No tasks.")
        self.assertIn("[done]", self.run_board("list", "--all").stdout)
        destination = self.directory / "export.csv"
        self.run_board("export", str(destination))
        with destination.open(encoding="utf-8", newline="") as output:
            rows = list(csv.reader(output))
        self.assertEqual(rows[1], ["1", "Read, then revise", "2026-12-15", "done"])
        duplicate = self.run_board("export", str(destination), check=False)
        self.assertEqual(duplicate.returncode, 1)

    def test_invalid_date_is_rejected(self):
        result = self.run_board("add", "Read", "--due", "2026-02-30", check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("use YYYY-MM-DD", result.stderr)


if __name__ == "__main__":
    unittest.main()
