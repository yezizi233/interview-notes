from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

import requests


USER_AGENT = "InterviewNotesSkill/1.0 (contact: interview-notes@example.com)"
DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/plain, */*",
}
SEC_HEADERS = {
    **DEFAULT_HEADERS,
    "Accept-Encoding": "gzip, deflate",
    "From": "interview-notes@example.com",
    "Referer": "https://www.sec.gov/",
}
COMPANY_SUFFIXES = {
    "inc",
    "incorporated",
    "corp",
    "corporation",
    "co",
    "company",
    "ltd",
    "limited",
    "llc",
    "plc",
    "holdings",
    "holding",
    "sa",
    "nv",
    "ag",
    "bv",
}


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


def _normalize_words(value: str) -> list[str]:
    cleaned = value.casefold().replace("&", " and ")
    cleaned = re.sub(r"[’']", "", cleaned)
    cleaned = re.sub(r"[^a-z0-9]+", " ", cleaned)
    return [token for token in cleaned.split() if token]


def _collapse_key(value: str) -> str:
    return "".join(_normalize_words(value))


def _strip_company_suffixes(tokens: list[str]) -> list[str]:
    trimmed = tokens[:]
    while trimmed and trimmed[-1] in COMPANY_SUFFIXES:
        trimmed.pop()
    return trimmed


def _company_keys(value: str) -> set[str]:
    tokens = _normalize_words(value)
    keys = set()
    collapsed = "".join(tokens)
    if len(collapsed) >= 3:
        keys.add(collapsed)
    stripped = "".join(_strip_company_suffixes(tokens))
    if len(stripped) >= 3:
        keys.add(stripped)
    return keys


def _unique_match(keys: set[str], index: dict[str, set[str]]) -> tuple[str | None, str]:
    matches: set[str] = set()
    for key in keys:
        matches.update(index.get(key, set()))
    if len(matches) == 1:
        return next(iter(matches)), ""
    if len(matches) > 1:
        preview = ", ".join(sorted(matches)[:3])
        return None, f"Ambiguous match across official names: {preview}"
    return None, ""


class ClinicalTrialsAdapter(VerificationAdapter):
    authority_name = "ClinicalTrials.gov"

    def can_handle(self, term: str) -> bool:
        return bool(re.fullmatch(r"NCT\d{8}", term))

    def verify(self, term: str) -> VerificationRecord:
        response = requests.get(
            "https://clinicaltrials.gov/api/v2/studies",
            params={
                "query.id": term,
                "pageSize": 1,
                "fields": "protocolSection.identificationModule",
            },
            headers=DEFAULT_HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        studies = payload.get("studies", [])
        if not studies:
            return VerificationRecord(
                raw=term,
                normalized=term,
                status="unverified",
                authority=self.authority_name,
                note="No ClinicalTrials.gov study matched this identifier.",
            )

        identification = studies[0].get("protocolSection", {}).get("identificationModule", {})
        normalized = identification.get("officialTitle") or identification.get("briefTitle") or term
        return VerificationRecord(
            raw=term,
            normalized=normalized,
            status="verified online",
            authority=self.authority_name,
        )


class SecCompanyAdapter(VerificationAdapter):
    authority_name = "SEC EDGAR"

    def can_handle(self, term: str) -> bool:
        return bool(re.search(r"[A-Za-z]", term)) and len(term.strip()) >= 2

    def verify(self, term: str) -> VerificationRecord:
        by_ticker, by_name, load_error = self._load_company_index()
        if load_error:
            return VerificationRecord(
                raw=term,
                normalized=term,
                status="unverified",
                authority=self.authority_name,
                note=load_error,
            )
        query = term.strip()
        ticker = query.upper()
        if ticker in by_ticker:
            return VerificationRecord(
                raw=term,
                normalized=by_ticker[ticker],
                status="verified online",
                authority=self.authority_name,
            )

        match, note = _unique_match(_company_keys(query), by_name)
        if match:
            return VerificationRecord(
                raw=term,
                normalized=match,
                status="verified online",
                authority=self.authority_name,
            )
        return VerificationRecord(
            raw=term,
            normalized=term,
            status="unverified",
            authority=self.authority_name,
            note=note or "No exact SEC public-company match was found.",
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def _load_company_index() -> tuple[dict[str, str], dict[str, set[str]], str]:
        by_ticker: dict[str, str] = {}
        by_name: dict[str, set[str]] = {}
        errors: list[str] = []
        for url in (
            "https://www.sec.gov/files/company_tickers_exchange.json",
            "https://www.sec.gov/files/company_tickers.json",
        ):
            try:
                response = requests.get(
                    url,
                    headers=SEC_HEADERS,
                    timeout=15,
                )
                response.raise_for_status()
                payload = response.json()
                if "data" in payload:
                    rows = payload.get("data", [])
                    for row in rows:
                        if len(row) < 3:
                            continue
                        name = str(row[1]).strip()
                        ticker = str(row[2]).strip().upper()
                        if not name or not ticker:
                            continue
                        by_ticker[ticker] = name
                        for key in _company_keys(name):
                            by_name.setdefault(key, set()).add(name)
                else:
                    for row in payload.values():
                        name = str(row.get("title", "")).strip()
                        ticker = str(row.get("ticker", "")).strip().upper()
                        if not name or not ticker:
                            continue
                        by_ticker[ticker] = name
                        for key in _company_keys(name):
                            by_name.setdefault(key, set()).add(name)
                if by_ticker:
                    return by_ticker, by_name, ""
            except requests.RequestException as exc:
                errors.append(f"{url}: {exc}")
        error_note = "SEC company index unavailable. " + " | ".join(errors)
        return {}, {}, error_note


class DailyMedDrugNameAdapter(VerificationAdapter):
    authority_name = "DailyMed"

    def can_handle(self, term: str) -> bool:
        return bool(re.search(r"[A-Za-z]", term)) and 3 <= len(term.strip()) <= 80

    def verify(self, term: str) -> VerificationRecord:
        query_keys = {_collapse_key(term)}
        matches: set[str] = set()
        for name_type in ("brand", "generic"):
            payload = self._lookup(term, name_type)
            for item in payload.get("data", []):
                drug_name = str(item.get("drug_name", "")).strip()
                if not drug_name:
                    continue
                if _collapse_key(drug_name) in query_keys:
                    matches.add(drug_name)

        if len(matches) == 1:
            return VerificationRecord(
                raw=term,
                normalized=next(iter(matches)),
                status="verified online",
                authority=self.authority_name,
            )
        if len(matches) > 1:
            preview = ", ".join(sorted(matches)[:3])
            return VerificationRecord(
                raw=term,
                normalized=term,
                status="unverified",
                authority=self.authority_name,
                note=f"Ambiguous DailyMed match across official drug names: {preview}",
            )
        return VerificationRecord(
            raw=term,
            normalized=term,
            status="unverified",
            authority=self.authority_name,
            note="No exact DailyMed drug-name match was found.",
        )

    @staticmethod
    @lru_cache(maxsize=256)
    def _lookup(term: str, name_type: str) -> dict:
        response = requests.get(
            "https://dailymed.nlm.nih.gov/dailymed/services/v2/drugnames.json",
            params={
                "drug_name": term,
                "name_type": name_type,
                "pagesize": 10,
                "page": 1,
            },
            headers=DEFAULT_HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()


class ClinicalTrialsSponsorAdapter(VerificationAdapter):
    authority_name = "ClinicalTrials.gov sponsor registry"

    def can_handle(self, term: str) -> bool:
        return bool(re.search(r"[A-Za-z]", term)) and 3 <= len(term.strip()) <= 120

    def verify(self, term: str) -> VerificationRecord:
        payload = self._lookup(term)
        query_key = _collapse_key(term)
        matches: set[str] = set()
        for study in payload.get("studies", []):
            protocol = study.get("protocolSection", {})
            identification = protocol.get("identificationModule", {})
            sponsor_module = protocol.get("sponsorCollaboratorsModule", {})
            candidates = [
                identification.get("organization", {}).get("fullName", ""),
                sponsor_module.get("leadSponsor", {}).get("name", ""),
            ]
            for collaborator in sponsor_module.get("collaborators", []):
                candidates.append(str(collaborator.get("name", "")).strip())
            for candidate in candidates:
                candidate = str(candidate).strip()
                if candidate and _collapse_key(candidate) == query_key:
                    matches.add(candidate)

        if len(matches) == 1:
            return VerificationRecord(
                raw=term,
                normalized=next(iter(matches)),
                status="verified online",
                authority=self.authority_name,
            )
        if len(matches) > 1:
            preview = ", ".join(sorted(matches)[:3])
            return VerificationRecord(
                raw=term,
                normalized=term,
                status="unverified",
                authority=self.authority_name,
                note=f"Ambiguous ClinicalTrials.gov sponsor match: {preview}",
            )
        return VerificationRecord(
            raw=term,
            normalized=term,
            status="unverified",
            authority=self.authority_name,
            note="No exact ClinicalTrials.gov sponsor or collaborator match was found.",
        )

    @staticmethod
    @lru_cache(maxsize=256)
    def _lookup(term: str) -> dict:
        response = requests.get(
            "https://clinicaltrials.gov/api/v2/studies",
            params={
                "query.spons": term,
                "pageSize": 10,
                "fields": "protocolSection.identificationModule,protocolSection.sponsorCollaboratorsModule",
            },
            headers=DEFAULT_HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()


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
    SecCompanyAdapter(),
    DailyMedDrugNameAdapter(),
    ClinicalTrialsSponsorAdapter(),
]
FALLBACK_ADAPTER = PassthroughAdapter()


def _record_rank(record: VerificationRecord) -> int:
    if record.status == "verified online":
        return 3
    if record.authority:
        return 2
    return 1


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
        best_record: VerificationRecord | None = None
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
            if best_record is None or _record_rank(record) > _record_rank(best_record):
                best_record = record
            if record.status == "verified online":
                break
        results[term] = best_record or FALLBACK_ADAPTER.verify(term)

    if any(value.status == "unverified" for value in results.values()):
        notices.append(
            "Some company/product/institution names remain unverified. Current automatic verification supports SEC public-company names and tickers, DailyMed drug names, ClinicalTrials.gov trial IDs, and ClinicalTrials.gov sponsor or collaborator names."
        )
    return results, notices
