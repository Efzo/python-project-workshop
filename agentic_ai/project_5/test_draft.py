from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from draft import run


class ApprovalEvals(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(TemporaryDirectory())
        self.output = Path(directory) / "out"

    def test_preview_is_relevant_and_leaves_no_files(self):
        preview = run("loops", self.output, approved=False)
        self.assertIn("for loop", preview)
        self.assertFalse(self.output.exists())

    def test_approval_saves_once(self):
        run("loops", self.output, approved=True)
        file = self.output / "exercise.txt"
        original = file.read_text()
        with self.assertRaises(FileExistsError):
            run("files", self.output, approved=True)
        self.assertEqual(file.read_text(), original)

    def test_unsupported_topic_creates_nothing(self):
        with self.assertRaises(ValueError):
            run("algebra", self.output, approved=True)
        self.assertFalse(self.output.exists())
