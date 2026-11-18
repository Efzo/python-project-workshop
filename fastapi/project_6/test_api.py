from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fastapi.testclient import TestClient
from study_api.main import create_app


class StudyApiTests(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(TemporaryDirectory())
        self.db_path = Path(directory) / "study.db"
        self.headers = {"Authorization": "Bearer test-secret"}

    def client(self):
        return TestClient(create_app(self.db_path, "test-secret"))

    def test_round_trip_through_restart(self):
        with self.client() as client:
            health = client.get("/health")
            self.assertEqual(health.json(), {"status": "ok"})
            self.assertIn("X-Response-Time-Ms", health.headers)
            created = client.post("/v1/tasks", json={"title": "Study FastAPI"}, headers=self.headers)
            self.assertEqual(created.status_code, 201)
            task_id = created.json()["id"]
        with self.client() as client:
            changed = client.patch(f"/v1/tasks/{task_id}", json={"done": True}, headers=self.headers)
            self.assertEqual(changed.status_code, 200)
            self.assertTrue(changed.json()["done"])
            listed = client.get("/v1/tasks?limit=1&offset=0", headers=self.headers)
            self.assertEqual(listed.json()[0]["title"], "Study FastAPI")

    def test_auth_validation_and_missing_id(self):
        with self.client() as client:
            self.assertEqual(client.get("/v1/tasks").status_code, 401)
            self.assertEqual(client.get("/v1/tasks?limit=0", headers=self.headers).status_code, 422)
            missing = client.patch("/v1/tasks/99", json={"done": True}, headers=self.headers)
            self.assertEqual(missing.status_code, 404)
