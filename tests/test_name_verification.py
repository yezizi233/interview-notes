from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "interview-notes" / "scripts"
import sys

sys.path.insert(0, str(SCRIPTS_DIR))

from name_verification.registry import (  # noqa: E402
    ClinicalTrialsSponsorAdapter,
    DailyMedDrugNameAdapter,
    SecCompanyAdapter,
    verify_terms_with_adapters,
)


class FakeResponse:
    def __init__(self, payload: dict, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def json(self) -> dict:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class NameVerificationTest(unittest.TestCase):
    def setUp(self) -> None:
        SecCompanyAdapter._load_company_index.cache_clear()
        DailyMedDrugNameAdapter._lookup.cache_clear()
        ClinicalTrialsSponsorAdapter._lookup.cache_clear()

    @patch("name_verification.registry.requests.get")
    def test_sec_adapter_verifies_ticker_and_company_name(self, mock_get) -> None:
        mock_get.return_value = FakeResponse(
            {
                "fields": ["cik", "name", "ticker", "exchange"],
                "data": [
                    [320193, "Apple Inc.", "AAPL", "Nasdaq"],
                    [1652044, "Alphabet Inc.", "GOOGL", "Nasdaq"],
                ],
            }
        )

        results, notices = verify_terms_with_adapters(["AAPL", "Apple"], network_available=True)

        self.assertEqual(results["AAPL"].normalized, "Apple Inc.")
        self.assertEqual(results["Apple"].normalized, "Apple Inc.")
        self.assertEqual(results["Apple"].authority, "SEC EDGAR")
        self.assertTrue(all(record.status == "verified online" for record in results.values()))
        self.assertFalse(notices)

    @patch("name_verification.registry.requests.get")
    def test_dailymed_adapter_verifies_product_name_after_sec_miss(self, mock_get) -> None:
        def fake_get(url, params=None, headers=None, timeout=None):  # noqa: ANN001
            if "company_tickers_exchange.json" in url or "company_tickers.json" in url:
                return FakeResponse({"fields": ["cik", "name", "ticker", "exchange"], "data": []})
            if "dailymed" in url:
                name_type = params["name_type"]
                if name_type == "brand":
                    return FakeResponse({"data": [{"drug_name": "LIPITOR", "name_type": "B"}]})
                return FakeResponse({"data": []})
            raise AssertionError(f"Unexpected URL: {url}")

        mock_get.side_effect = fake_get

        results, notices = verify_terms_with_adapters(["Lipitor"], network_available=True)

        self.assertEqual(results["Lipitor"].normalized, "LIPITOR")
        self.assertEqual(results["Lipitor"].authority, "DailyMed")
        self.assertEqual(results["Lipitor"].status, "verified online")
        self.assertFalse(notices)

    @patch("name_verification.registry.requests.get")
    def test_clinicaltrials_sponsor_adapter_verifies_institution_name(self, mock_get) -> None:
        def fake_get(url, params=None, headers=None, timeout=None):  # noqa: ANN001
            if "company_tickers_exchange.json" in url or "company_tickers.json" in url:
                return FakeResponse({"fields": ["cik", "name", "ticker", "exchange"], "data": []})
            if "dailymed" in url:
                return FakeResponse({"data": []})
            if "clinicaltrials.gov/api/v2/studies" in url and params.get("query.spons") == "GlaxoSmithKline":
                return FakeResponse(
                    {
                        "studies": [
                            {
                                "protocolSection": {
                                    "identificationModule": {
                                        "organization": {"fullName": "GlaxoSmithKline"}
                                    },
                                    "sponsorCollaboratorsModule": {
                                        "leadSponsor": {"name": "GlaxoSmithKline", "class": "INDUSTRY"},
                                        "collaborators": [],
                                    },
                                }
                            }
                        ]
                    }
                )
            raise AssertionError(f"Unexpected URL or params: {url} {params}")

        mock_get.side_effect = fake_get

        results, notices = verify_terms_with_adapters(["GlaxoSmithKline"], network_available=True)

        self.assertEqual(results["GlaxoSmithKline"].normalized, "GlaxoSmithKline")
        self.assertEqual(results["GlaxoSmithKline"].authority, "ClinicalTrials.gov sponsor registry")
        self.assertEqual(results["GlaxoSmithKline"].status, "verified online")
        self.assertFalse(notices)

    @patch("name_verification.registry.requests.get")
    def test_unverified_terms_emit_updated_coverage_notice(self, mock_get) -> None:
        def fake_get(url, params=None, headers=None, timeout=None):  # noqa: ANN001
            if "company_tickers_exchange.json" in url or "company_tickers.json" in url:
                return FakeResponse({"fields": ["cik", "name", "ticker", "exchange"], "data": []})
            if "dailymed" in url:
                return FakeResponse({"data": []})
            if "clinicaltrials.gov/api/v2/studies" in url:
                return FakeResponse({"studies": []})
            raise AssertionError(f"Unexpected URL: {url}")

        mock_get.side_effect = fake_get

        results, notices = verify_terms_with_adapters(["Unknown Labs"], network_available=True)

        self.assertEqual(results["Unknown Labs"].status, "unverified")
        self.assertTrue(
            any("SEC public-company names and tickers" in notice and "DailyMed drug names" in notice for notice in notices)
        )


if __name__ == "__main__":
    unittest.main()
