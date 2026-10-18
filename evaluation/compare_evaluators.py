
import json
from pathlib import Path

from evaluation.dataset import load_dataset
from evaluation.metrics import classification_metrics

DATASET = Path("data/eval/claim_citations.jsonl")
NLI_PREDICTIONS = Path("results/nli_predictions.jsonl")
LLM_PREDICTIONS = Path("results/llm_judge_predictions.jsonl")
OUTPUT = Path("results/evaluator_comparison.json")


def load_predictions(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(
            f"Predictions not found: {path}. Run that evaluator first."
        )

    predictions = {}
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {path}, line {line_number}: {exc}"
                ) from exc

            if not {"id", "prediction"} <= item.keys():
                raise ValueError(
                    f"{path}, line {line_number}: expected id and prediction"
                )

            if item["id"] in predictions:
                raise ValueError(f"Duplicate prediction id: {item['id']}")

            predictions[item["id"]] = item["prediction"]

    return predictions


def evaluate_predictions(
    records: list[dict],
    predictions: dict[str, str],
) -> dict:
    expected_ids = {record["id"] for record in records}
    actual_ids = set(predictions)

    if expected_ids != actual_ids:
        raise ValueError(
            f"Prediction IDs mismatch. Missing={sorted(expected_ids - actual_ids)}, "
            f"extra={sorted(actual_ids - expected_ids)}"
        )

    by_id = {record["id"]: record for record in records}
    ordered_ids = [record["id"] for record in records]

    return classification_metrics(
        [by_id[item_id]["label"] for item_id in ordered_ids],
        [predictions[item_id] for item_id in ordered_ids],
    )


def main():
    records = load_dataset(DATASET)

    nli_predictions = load_predictions(NLI_PREDICTIONS)
    llm_predictions = load_predictions(LLM_PREDICTIONS)

    report = {
        "dataset_size": len(records),
        "nli": evaluate_predictions(records, nli_predictions),
        "llm_judge": evaluate_predictions(records, llm_predictions),
        "note": (
            "Comparison is meaningful only if both evaluators use the same "
            "examples and label definitions."
        ),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    print(f"\nSaved comparison to {OUTPUT}")


if __name__ == "__main__":
    main()
