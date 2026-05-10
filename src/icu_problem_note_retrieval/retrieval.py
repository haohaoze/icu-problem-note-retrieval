from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from .matching import build_terms_by_field, find_hits
from .types import ExpansionRecord, Note, RetrievedNote, TermHit


FIELD_WEIGHTS = {
    "aliases": 1.0,
    "query_expressions": 1.1,
    "evidence_search_terms": 1.2,
}


def candidate_notes(
    notes: Iterable[Note],
    *,
    current_patient_id: str,
    current_time: datetime,
) -> tuple[Note, ...]:
    candidates = [
        note
        for note in notes
        if note.patient_id == current_patient_id and note.note_time < current_time
    ]
    return tuple(sorted(candidates, key=lambda note: (note.note_time, note.note_id)))


def score_hits(hits: tuple[TermHit, ...]) -> float:
    unique_field_terms = {(hit.field, hit.term) for hit in hits}
    unique_score = sum(FIELD_WEIGHTS.get(field, 1.0) for field, _ in unique_field_terms)
    repeat_bonus = max(0, len(hits) - len(unique_field_terms)) * 0.05
    return round(unique_score + repeat_bonus, 6)


def retrieve_all_hits(
    expansion: ExpansionRecord,
    notes: Iterable[Note],
    *,
    current_patient_id: str,
    current_time: datetime,
) -> tuple[RetrievedNote, ...]:
    terms_by_field = build_terms_by_field(expansion)
    retrieved: list[RetrievedNote] = []
    for note in candidate_notes(
        notes,
        current_patient_id=current_patient_id,
        current_time=current_time,
    ):
        hits = find_hits(note.text, terms_by_field)
        if hits:
            retrieved.append(RetrievedNote(note=note, hits=hits, score=score_hits(hits)))
    return tuple(
        sorted(
            retrieved,
            key=lambda item: (-item.score, item.note.note_time, item.note.note_id),
        )
    )


def retrieve_fixed_k(
    expansion: ExpansionRecord,
    notes: Iterable[Note],
    *,
    current_patient_id: str,
    current_time: datetime,
    k: int,
) -> tuple[RetrievedNote, ...]:
    if k < 0:
        raise ValueError("k must be non-negative")
    return retrieve_all_hits(
        expansion,
        notes,
        current_patient_id=current_patient_id,
        current_time=current_time,
    )[:k]

