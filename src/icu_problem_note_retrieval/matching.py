from __future__ import annotations

import re
from collections.abc import Mapping

from .filters import filter_expansion
from .types import ExpansionRecord, TermHit


EXPANSION_FIELDS = ("aliases", "query_expressions", "evidence_search_terms")


def build_terms_by_field(expansion: ExpansionRecord) -> dict[str, tuple[str, ...]]:
    filtered = filter_expansion(expansion)
    return {
        "aliases": filtered.aliases,
        "query_expressions": filtered.query_expressions,
        "evidence_search_terms": filtered.evidence_search_terms,
    }


def compile_boundary_pattern(term: str) -> re.Pattern[str]:
    escaped_tokens = [re.escape(token) for token in term.split()]
    body = r"\s+".join(escaped_tokens)
    return re.compile(rf"(?<![A-Za-z0-9]){body}(?![A-Za-z0-9])", re.IGNORECASE)


def find_hits(text: str, terms_by_field: Mapping[str, tuple[str, ...]]) -> tuple[TermHit, ...]:
    hits: list[TermHit] = []
    for field in EXPANSION_FIELDS:
        for term in terms_by_field.get(field, ()):
            pattern = compile_boundary_pattern(term)
            for match in pattern.finditer(text):
                hits.append(
                    TermHit(
                        field=field,
                        term=term,
                        start=match.start(),
                        end=match.end(),
                        matched_text=match.group(0),
                    )
                )
    return tuple(sorted(hits, key=lambda hit: (hit.start, hit.end, hit.field, hit.term)))

