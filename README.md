# ICU Problem Note Retrieval

Minimal deterministic code for problem-centric historical ICU note retrieval.

Given a current ICU active problem and a set of historical notes from the same
patient, the package retrieves earlier notes that contain valid frozen expansion
terms for that problem.

## What is included

- same-patient historical-note filtering
- deterministic expansion-term filtering
- boundary-aware keyword matching
- all-hit retrieval
- fixed-k truncation by keyword-hit strength
- small synthetic examples and unit tests

## Model handling

No model is run during retrieval.

The intended workflow is:

1. Generate lexical expansions offline for each problem.
2. Freeze the resulting terms before validation or review.
3. Store only structured terms such as aliases, query expressions, and evidence
   search terms.
4. Run this package as a deterministic matcher over same-patient historical notes.

The package does not include model weights, API keys, prompts, patient-specific
model calls, or patient-note text. The retrieval functions do not use a model to
read notes, rank notes, label notes, or make patient-specific clinical judgments.

## Data policy

Patient-level clinical notes are not included. The files in `examples/` are
synthetic and are only for testing the code path.

Studies using MIMIC-III or similar clinical databases should keep data outside
this repository and follow the relevant data use agreement. Patient-level notes
should not be redistributed.

## Quick start

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

```python
from datetime import datetime
from icu_problem_note_retrieval import ExpansionRecord, Note, retrieve_all_hits

problem = ExpansionRecord(
    problem_id="aki",
    problem_text="acute kidney injury",
    aliases=("AKI",),
    query_expressions=("acute kidney injury",),
    evidence_search_terms=("creatinine rise",),
)

notes = [
    Note("n1", "p1", datetime.fromisoformat("2020-01-01T08:00:00"), "AKI with creatinine rise."),
    Note("n2", "p2", datetime.fromisoformat("2020-01-01T08:00:00"), "AKI mentioned in another patient."),
]

hits = retrieve_all_hits(
    problem,
    notes,
    current_patient_id="p1",
    current_time=datetime.fromisoformat("2020-01-02T08:00:00"),
)
```
