
import json
from collections import Counter
from pathlib import Path

from evaluation.dataset import load_dataset

DATASET_PATH = Path("data/eval/claim_citations.jsonl")
RESULTS_PATH = Path("results/manual_baseline.json")


def main():
    records = load_dataset(DATASET_PATH)
    label_counts = Counter(record["label"] for record in records)

    report = {
        "evaluation_type": "manual_dataset_validation",
        "dataset": str(DATASET_PATH),
        "total_examples": len(records),
        "label_counts": dict(label_counts),
        "status": "validated; model evaluation not yet run",
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    print(f"\nSaved report to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
