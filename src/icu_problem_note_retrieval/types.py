from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping


@dataclass(frozen=True)
class Note:
    note_id: str
    patient_id: str
    note_time: datetime
    text: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExpansionRecord:
    problem_id: str
    problem_text: str
    aliases: tuple[str, ...] = ()
    query_expressions: tuple[str, ...] = ()
    evidence_search_terms: tuple[str, ...] = ()


@dataclass(frozen=True)
class TermHit:
    field: str
    term: str
    start: int
    end: int
    matched_text: str


@dataclass(frozen=True)
class RetrievedNote:
    note: Note
    hits: tuple[TermHit, ...]
    score: float

