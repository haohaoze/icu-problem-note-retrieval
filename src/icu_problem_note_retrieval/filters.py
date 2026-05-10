from __future__ import annotations

import re

from .text import normalize_term, unique_normalized_terms
from .types import ExpansionRecord


_ALPHA_RE = re.compile(r"[a-z]")

DEFAULT_BLOCKED_TERMS = frozenset(
    {
        "acute",
        "chronic",
        "current",
        "disease",
        "failure",
        "history",
        "issue",
        "medical",
        "new",
        "old",
        "patient",
        "problem",
        "status",
        "syndrome",
    }
)

DEFAULT_MIN_CHARS = 3


def is_valid_term(
    term: str,
    *,
    blocked_terms: frozenset[str] = DEFAULT_BLOCKED_TERMS,
    min_chars: int = DEFAULT_MIN_CHARS,
) -> bool:
    normalized = normalize_term(term)
    if len(normalized) < min_chars:
        return False
    if not _ALPHA_RE.search(normalized):
        return False
    if normalized in blocked_terms:
        return False
    tokens = normalized.split()
    if len(tokens) == 1 and tokens[0] in blocked_terms:
        return False
    return True


def filter_terms(terms: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(term for term in unique_normalized_terms(terms) if is_valid_term(term))


def filter_expansion(expansion: ExpansionRecord) -> ExpansionRecord:
    return ExpansionRecord(
        problem_id=expansion.problem_id,
        problem_text=expansion.problem_text,
        aliases=filter_terms(expansion.aliases),
        query_expressions=filter_terms(expansion.query_expressions),
        evidence_search_terms=filter_terms(expansion.evidence_search_terms),
    )

