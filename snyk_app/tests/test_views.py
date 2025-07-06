from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from snyk_app.models import Finding

# ? Example CMD to run the tests : docker compose exec snyk_django python manage.py test


class FindingListViewTests(APITestCase):
    # unit tests for the API - finding listing

    def setUp(self):
        # 2 sample Findings w/ dummy data
        Finding.objects.create(
            id=1,
            target_id="target-1",
            definition_id="def-123",
            scans=["scan-1", "scan-2"],
            url="https://example.com/1",
            path="/vuln/path1",
            method="GET",
        )
        Finding.objects.create(
            id=2,
            target_id="target-1",
            definition_id="def-456",
            scans=["scan-3"],
            url="https://example.com/2",
            path="/vuln/path2",
            method="POST",
        )

    def test_list_all_findings(self):
        response = self.client.get(reverse("findings-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["findings_count"], 2)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_by_definition_id(self):
        response = self.client.get(
            reverse("findings-list"), {"definition_id": "def-123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["findings_count"], 1)
        self.assertEqual(response.data["results"][0]["definition_id"], "def-123")

    def test_filter_by_scan(self):
        response = self.client.get(reverse("findings-list"), {"scan": "scan-1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["findings_count"], 1)
        self.assertIn("scan-1", response.data["results"][0]["scans"])

    def test_filter_by_invalid_scan(self):
        response = self.client.get(
            reverse("findings-list"), {"scan": "nonexistent-scan"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["findings_count"], 0)
