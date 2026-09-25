"""Prepare an answer-free case packet; never manufacture independent labels."""
from __future__ import annotations

import csv
import hashlib
from io import StringIO
import json
from pathlib import Path
import random
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DESTINATION = ROOT / "experiments/source_review_2026-09-25"
FIELDS = ["case_id", "source_sha256", "reviewer", "reviewed_utc", "finite_domain_label",
          "unbounded_scope", "reason", "counterexample"]
INSTRUCTIONS = """# Independent case review

Status: awaiting an external reviewer. This packet contains no analyzer predictions,
runtime labels, accuracy counts or original descriptive filenames. Do not open
the full repository's benchmark outputs or explanatory results PDF before labeling.
The sources themselves necessarily show their behavior; this is answer masking,
not double blinding or proof of reviewer independence.

Review the 24 cases without executing unknown source. Entry: implementation.
Use 64 integer record IDs 0 through 63, master 92591, 512 input dimensions and
64 output dimensions. The records are distinct. Other context arguments are fixed.
Imported BioHash/KDF/projection functions follow the supplied repository contracts:
generate_key hashes the UTF-8 string biohash:master:domain:index with SHA-256,
then takes the first eight digest bytes as an unsigned little-endian integer.
biohash uses one key for the whole projection; correlated_biohash shares the given
prefix width and uses the private key for the remaining columns. A zero-width
component does not count. Explicit projection concatenation joins component blocks.
For exact finite labels, compare component key labels, not accidental equal output
bits. A runtime audit may be used after an initial manual assessment; record it in
the reason. This is not a claim of actual biometric leakage.

Fill labels.csv. finite_domain_label: reuse_observed, no_reuse_observed, or unsure.
unbounded_scope: fixed, finite_pool, injective_under_contract, or unknown.
State assumptions, reasoning and any counterexample. Reviewer name and UTC date
are required for all entries. Unsure is valid and must not be silently forced to
safe. Do not let the analyzer choose your label. Authors must disclose prior
exposure to predictions and any conflict of interest.

Two reviewers should independently label separate copies. An adjudicator resolves
disagreements only after both copies are frozen and hashed. Retain originals and
adjudication reasons. Report agreement and uncertain cases, not only decided cases.
Add genuinely new cases in a separate package before seeing analyzer outcomes;
provide source, language assumptions, labels and counterexamples. The existing
24 cases are author-written development cases, not an independent holdout.

Return the completed CSV and review notes. Nothing is sent automatically. The
coordinator retains the original-to-neutral ID mapping separately. The independent
review gate remains pending until real external assessments have been received.
"""


def validate_labels(text: str, expected: dict[str, str]) -> list[dict]:
    rows = list(csv.DictReader(StringIO(text)))
    if len(rows) != len(expected) or {row.get("case_id") for row in rows} != set(expected):
        raise ValueError("Exactly one row per expected case is required")
    for row in rows:
        if row.get("source_sha256") != expected[row["case_id"]]:
            raise ValueError("Source hash mismatch")
        if not all(row.get(field, "").strip() for field in ["reviewer", "reviewed_utc", "reason"]):
            raise ValueError("External reviewer, date and reason are required; blank forms are not labels")
        if row.get("finite_domain_label") not in {"reuse_observed", "no_reuse_observed", "unsure"}:
            raise ValueError("Invalid finite-domain label")
        if row.get("unbounded_scope") not in {"fixed", "finite_pool", "injective_under_contract", "unknown"}:
            raise ValueError("Invalid unbounded-scope label")
    return rows


def build_packet(destination: Path = DESTINATION, coordinator: Path | None = None) -> dict:
    if destination.exists():
        raise FileExistsError("Review packet already exists")
    corpus = json.loads((ROOT / "experiments/source_security_utility_2026-09-25/benchmark/corpus.json").read_text())
    random.Random(92857).shuffle(corpus)
    rows, mapping, contents = [], [], {}
    for index, case in enumerate(corpus, 1):
        case_id = f"case_{index:03d}"
        source = case["source"].encode("utf-8")
        digest = hashlib.sha256(source).hexdigest()
        rows.append(dict.fromkeys(FIELDS, "") | {"case_id": case_id, "source_sha256": digest})
        mapping.append({"case_id": case_id, "original_case": case["case"], "source_sha256": digest})
        contents[f"cases/{case_id}.py"] = source
    csv_buffer = StringIO(newline="")
    writer = csv.DictWriter(csv_buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    contents["labels.csv"] = csv_buffer.getvalue().encode("utf-8")
    contents["README.md"] = INSTRUCTIONS.encode("ascii")
    destination.mkdir(parents=True)
    archive_path = destination / "independent_cases.zip"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in contents.items():
            archive.writestr(name, content)
    coordinator = coordinator or ROOT / "results/source_review_2026-09-25"
    coordinator.mkdir(parents=True, exist_ok=True)
    (coordinator / "coordinator_mapping.json").write_text(json.dumps(mapping, indent=2) + "\n")
    manifest = {"status": "awaiting_external_review", "cases": len(rows),
                "archive_sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
                "members_sha256": {name: hashlib.sha256(content).hexdigest() for name, content in contents.items()},
                "independent_labels_received": 0, "holdout_cases_received": 0,
                "blinding": "Predictions, oracle labels and original filenames withheld; source visible"}
    (destination / "packet_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(build_packet(), indent=2))