from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

from study_agent.providers import offline_answer, responses_answer


class StudyAgentTests(unittest.TestCase):
    def test_offline_uses_evidence_and_reports_missing_evidence(self):
        answer = offline_answer("Help me with loops", lambda _: None)
        self.assertEqual(answer.sources, ("loops",))
        self.assertIn("counting even numbers", answer.text)
        missing = offline_answer("What is photosynthesis?", lambda _: None)
        self.assertEqual(missing.sources, ())
        self.assertIn("No supporting", missing.text)

    def test_provider_receives_correlated_tool_result(self):
        client = Mock()
        tool_call = SimpleNamespace(
            type="function_call", name="read_note", arguments='{"note_id": "loops"}', call_id="call_1"
        )
        client.responses.create.side_effect = [
            SimpleNamespace(status="completed", output=[tool_call], output_text=""),
            SimpleNamespace(status="completed", output=[], output_text="Practice with a list [loops]."),
        ]
        answer = responses_answer("Teach me loops", lambda _: None, client, "test-model")
        result_item = client.responses.create.call_args.kwargs["input"][-1]
        self.assertEqual(result_item["call_id"], "call_1")
        self.assertIn("counting even numbers", result_item["output"])
        self.assertEqual(answer.sources, ("loops",))

    def test_history_and_export(self):
        with TemporaryDirectory() as directory:
            output = Path(directory)
            prefix = [sys.executable, "-m", "study_agent", "--db", str(output / "runs.db")]
            subprocess.run([*prefix, "ask", "Help with loops"], capture_output=True, check=True)
            history = subprocess.run([*prefix, "history"], capture_output=True, check=True, text=True)
            self.assertIn("1. [offline] Help with loops", history.stdout)
            export = output / "answer.txt"
            subprocess.run([*prefix, "export", "1", str(export)], capture_output=True, check=True)
            self.assertIn("Notes read: loops", export.read_text())
