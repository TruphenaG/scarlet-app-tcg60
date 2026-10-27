import os
from unittest.mock import patch

from django.db import OperationalError
from django.test import TestCase


class StatusPageTests(TestCase):
    def test_unconfigured_database_is_reported_without_false_success(self):
        with patch.dict(os.environ, {"STUDENT_NETID": "tcg60"}):
            response = self.client.get("/status/")

        self.assertContains(response, "tcg60")
        self.assertContains(response, "0 of 11 tables in order")
        self.assertContains(response, "not PostgreSQL")
        self.assertEqual(len(response.context["rows"]), 11)
        self.assertFalse(response.context["all_ok"])
        self.assertTrue(response.context["inline_ok"])
        for row in response.context["rows"]:
            with self.subTest(table=row["table"]):
                self.assertTrue(row["in_admin"])
                self.assertFalse(row["match_ok"])
                self.assertIn("table does not exist in this database", row["issues"])

    def test_missing_netid_is_visible(self):
        with patch.dict(os.environ, {"STUDENT_NETID": ""}):
            response = self.client.get("/status/")
        self.assertContains(response, "NOT SET")
        self.assertFalse(response.context["all_ok"])

    def test_database_outage_does_not_crash_status_page(self):
        with patch("pages.status.connection.cursor", side_effect=OperationalError("database unavailable")):
            response = self.client.get("/status/")
        self.assertContains(response, "The database could not be read")
        self.assertContains(response, "0 of 11 tables in order")
        self.assertFalse(response.context["all_ok"])

    def test_existing_public_pages_still_work(self):
        for path in ("/", "/catalog/", "/about/", "/contact/"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
