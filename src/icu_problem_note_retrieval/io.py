from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .types import ExpansionRecord, Note


def _read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_expansion(path: str | Path) -> ExpansionRecord:
    data = _read_json(path)
    return ExpansionRecord(
        problem_id=str(data["problem_id"]),
        problem_text=str(data["problem_text"]),
        aliases=tuple(data.get("aliases", ())),
        query_expressions=tuple(data.get("query_expressions", ())),
        evidence_search_terms=tuple(data.get("evidence_search_terms", ())),
    )


def load_notes(path: str | Path) -> tuple[Note, ...]:
    rows = _read_json(path)
    notes: list[Note] = []
    for row in rows:
        notes.append(
            Note(
                note_id=str(row["note_id"]),
                patient_id=str(row["patient_id"]),
                note_time=datetime.fromisoformat(str(row["note_time"])),
                text=str(row["text"]),
                metadata=dict(row.get("metadata", {})),
            )
        )
    return tuple(notes)

