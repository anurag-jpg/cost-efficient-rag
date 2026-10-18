
import json
from pathlib import Path

ALLOWED_LABELS = {
    "supported",
    "contradicted",
    "insufficient_evidence",
}

REQUIRED_FIELDS = {
    "id",
    "claim",
    "evidence",
    "label",
    "source",
    "page",
}


def load_dataset(path: str | Path) -> list[dict]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    records = []
    seen_ids = set()

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

            if not isinstance(record, dict):
                raise ValueError(
                    f"Line {line_number} must contain a JSON object."
                )

            missing = REQUIRED_FIELDS - record.keys()
            if missing:
                raise ValueError(
                    f"Line {line_number} is missing: {sorted(missing)}"
                )

            record_id = record["id"]
            if not isinstance(record_id, str) or not record_id.strip():
                raise ValueError(
                    f"Line {line_number}: id must be a non-empty string."
                )

            if record_id in seen_ids:
                raise ValueError(f"Duplicate id: {record_id}")

            seen_ids.add(record_id)

            for field in ("claim", "evidence", "source"):
                if not isinstance(record[field], str) or not record[field].strip():
                    raise ValueError(
                        f"Line {line_number}: {field} must be non-empty."
                    )

            if record["label"] not in ALLOWED_LABELS:
                raise ValueError(
                    f"Line {line_number}: invalid label "
                    f"{record['label']!r}"
                )

            if (
                not isinstance(record["page"], int)
                or isinstance(record["page"], bool)
                or record["page"] < 1
            ):
                raise ValueError(
                    f"Line {line_number}: page must be a positive integer."
                )

            records.append(record)

    if not records:
        raise ValueError("Dataset is empty.")

    return records
