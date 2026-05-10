from __future__ import annotations

import unittest
from datetime import datetime

from icu_problem_note_retrieval import (
    ExpansionRecord,
    Note,
    candidate_notes,
    find_hits,
    retrieve_all_hits,
    retrieve_fixed_k,
)
from icu_problem_note_retrieval.matching import build_terms_by_field


class RetrievalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.expansion = ExpansionRecord(
            problem_id="aki",
            problem_text="acute kidney injury",
            aliases=("AKI", "failure"),
            query_expressions=("acute kidney injury",),
            evidence_search_terms=("creatinine rise",),
        )
        self.notes = (
            Note(
                "n1",
                "p1",
                datetime.fromisoformat("2020-01-01T08:00:00"),
                "AKI with creatinine rise after hypotension.",
            ),
            Note(
                "n2",
                "p1",
                datetime.fromisoformat("2020-01-02T08:00:00"),
                "No relevant kidney phrase here.",
            ),
            Note(
                "n3",
                "p2",
                datetime.fromisoformat("2020-01-01T08:00:00"),
                "AKI in another patient.",
            ),
            Note(
                "n4",
                "p1",
                datetime.fromisoformat("2020-01-04T08:00:00"),
                "Future AKI note.",
            ),
        )

    def test_candidate_notes_are_same_patient_and_prior_only(self) -> None:
        candidates = candidate_notes(
            self.notes,
            current_patient_id="p1",
            current_time=datetime.fromisoformat("2020-01-03T08:00:00"),
        )
        self.assertEqual([note.note_id for note in candidates], ["n1", "n2"])

    def test_boundary_matching_does_not_match_inside_words(self) -> None:
        terms = build_terms_by_field(
            ExpansionRecord(
                problem_id="aki",
                problem_text="acute kidney injury",
                aliases=("AKI",),
            )
        )
        hits = find_hits("The word staking should not match aki.", terms)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].matched_text, "aki")

    def test_retrieve_all_hits(self) -> None:
        retrieved = retrieve_all_hits(
            self.expansion,
            self.notes,
            current_patient_id="p1",
            current_time=datetime.fromisoformat("2020-01-03T08:00:00"),
        )
        self.assertEqual([item.note.note_id for item in retrieved], ["n1"])
        self.assertGreater(retrieved[0].score, 1.0)

    def test_fixed_k_truncates_all_hits(self) -> None:
        retrieved = retrieve_fixed_k(
            self.expansion,
            self.notes,
            current_patient_id="p1",
            current_time=datetime.fromisoformat("2020-01-03T08:00:00"),
            k=0,
        )
        self.assertEqual(retrieved, ())


if __name__ == "__main__":
    unittest.main()

