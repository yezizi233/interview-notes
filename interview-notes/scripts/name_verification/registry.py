from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

import requests


@dataclass
class VerificationRecord:
    raw: str
    normalized: str
    status: str
    authority: str = ""
    note: str = ""


class VerificationAdapter:
    authority_name = ""

    def can_handle(self, term: str) -> bool:
        raise NotImplementedError

    def verify(self, term: str) -> VerificationRecord:
        raise NotImplementedError


class ClinicalTrialsAdapter(VerificationAdapter):
    authority_name = "ClinicalTrials.gov"

    def can_handle(self, term: str) -> bool:
        return bool(re.fullmatch(r"NCT\d{8}", term))

    def verify(self, term: str) -> VerificationRecord:
        response = requests.get(
            "https://clinicaltrials.gov/api/query/study_fields",
            params={
                "expr": term,
                "fields": "NCTId,BriefTitle,OfficialTitle",
                "min_rnk": 1,
                "max_rnk": 1,
                "fmt": "json",
            },
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        studies = payload.get("StudyFieldsResponse", {}).get("StudyFields", [])
        if not studies:
            return VerificationRecord(
                raw=term,
                normalized=term,
                status="unverified",
                authority=self.authority_name,
                note="No ClinicalTrials.gov study matched this identifier.",
            )

        study = studies[0]
        normalized = study.get("OfficialTitle", []) or study.get("BriefTitle", []) or [term]
        return VerificationRecord(
            raw=term,
            normalized=normalized[0],
            status="verified online",
            authority=self.authority_name,
        )


class PassthroughAdapter(VerificationAdapter):
    authority_name = ""

    def can_handle(self, term: str) -> bool:
        return True

    def verify(self, term: str) -> VerificationRecord:
        return VerificationRecord(
            raw=term,
            normalized=term,
            status="unverified",
            note="No authoritative adapter configured for this term.",
        )


ADAPTERS: list[VerificationAdapter] = [
    ClinicalTrialsAdapter(),
    PassthroughAdapter(),
]


def verify_terms_with_adapters(
    terms: Iterable[str],
    network_available: bool,
) -> tuple[dict[str, VerificationRecord], list[str]]:
    notices: list[str] = []
    results: dict[str, VerificationRecord] = {}

    if not network_available:
        notices.append("Network unavailable: online proper-name verification is disabled.")
        for term in terms:
            results[term] = VerificationRecord(
                raw=term,
                normalized=term,
                status="unverified offline",
            )
        return results, notices

    for term in terms:
        for adapter in ADAPTERS:
            if not adapter.can_handle(term):
                continue
            try:
                record = adapter.verify(term)
            except requests.RequestException as exc:
                notices.append(f"{adapter.authority_name or 'adapter'} lookup failed for {term}: {exc}")
                record = VerificationRecord(
                    raw=term,
                    normalized=term,
                    status="unverified",
                    authority=adapter.authority_name,
                    note=str(exc),
                )
            results[term] = record
            break

    if any(value.status == "unverified" for value in results.values()):
        notices.append(
            "Some company/product/institution names remain unverified. Current automatic verification supports ClinicalTrials.gov trial IDs; other terms are preserved and flagged as unverified."
        )
    return results, notices
