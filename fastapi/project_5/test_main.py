import unittest

from fastapi.testclient import TestClient

from main import Settings, app, load_settings


class MetricsTests(unittest.TestCase):
    def setUp(self):
        app.dependency_overrides[load_settings] = lambda: Settings(token="test-secret")
        self.addCleanup(app.dependency_overrides.clear)
        self.client = self.enterContext(TestClient(app))

    def test_unauthenticated_request(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers["WWW-Authenticate"], "Bearer")

    def test_valid_token_returns_metrics(self):
        response = self.client.get("/metrics", headers={"Authorization": "Bearer test-secret"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"queued": 3, "ready": 7})
