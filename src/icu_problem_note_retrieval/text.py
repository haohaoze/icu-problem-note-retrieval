from __future__ import annotations

import re
from collections.abc import Iterable


_SPACE_RE = re.compile(r"\s+")


def normalize_space(value: str) -> str:
    return _SPACE_RE.sub(" ", value.strip())


def normalize_term(term: str) -> str:
    return normalize_space(term).lower()


def unique_normalized_terms(terms: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    kept: list[str] = []
    for term in terms:
        normalized = normalize_term(term)
        if normalized and normalized not in seen:
            seen.add(normalized)
            kept.append(normalized)
    return tuple(kept)

