
from collections import Counter

LABELS = [
    "supported",
    "contradicted",
    "insufficient_evidence",
]


def classification_metrics(
    y_true: list[str],
    y_pred: list[str],
) -> dict:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have equal lengths.")

    if not y_true:
        raise ValueError("Cannot evaluate empty predictions.")

    invalid = (set(y_true) | set(y_pred)) - set(LABELS)
    if invalid:
        raise ValueError(f"Unknown labels: {sorted(invalid)}")

    per_class = {}
    f1_values = []

    for label in LABELS:
        tp = sum(
            actual == label and predicted == label
            for actual, predicted in zip(y_true, y_pred)
        )
        fp = sum(
            actual != label and predicted == label
            for actual, predicted in zip(y_true, y_pred)
        )
        fn = sum(
            actual == label and predicted != label
            for actual, predicted in zip(y_true, y_pred)
        )
        support = sum(actual == label for actual in y_true)

        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )

        per_class[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": support,
        }
        f1_values.append(f1)

    correct = sum(a == p for a, p in zip(y_true, y_pred))

    confusion = {
        actual: {
            predicted: sum(
                a == actual and p == predicted
                for a, p in zip(y_true, y_pred)
            )
            for predicted in LABELS
        }
        for actual in LABELS
    }

    return {
        "examples": len(y_true),
        "accuracy": round(correct / len(y_true), 4),
        "macro_f1": round(sum(f1_values) / len(f1_values), 4),
        "per_class": per_class,
        "confusion_matrix": confusion,
    }


def retrieval_metrics(
    relevant_ids: set[str],
    ranked_ids: list[str],
    k: int = 5,
) -> dict:
    """Evaluate one query's ranked retrieval results."""
    if k < 1:
        raise ValueError("k must be >= 1.")

    ranked = ranked_ids[:k]
    relevant_count = len(relevant_ids)

    hits = [doc_id in relevant_ids for doc_id in ranked]
    hit_rate = float(any(hits))

    recall = (
        sum(hits) / relevant_count if relevant_count else 0.0
    )

    reciprocal_rank = 0.0
    for rank, is_relevant in enumerate(hits, start=1):
        if is_relevant:
            reciprocal_rank = 1.0 / rank
            break

    dcg = sum(
        1.0 / __import__("math").log2(rank + 1)
        for rank, is_relevant in enumerate(hits, start=1)
        if is_relevant
    )
    ideal_hits = min(relevant_count, k)
    ideal_dcg = sum(
        1.0 / __import__("math").log2(rank + 1)
        for rank in range(1, ideal_hits + 1)
    )

    return {
        f"recall@{k}": round(recall, 4),
        f"hit_rate@{k}": round(hit_rate, 4),
        "reciprocal_rank": round(reciprocal_rank, 4),
        f"ndcg@{k}": round(dcg / ideal_dcg, 4) if ideal_dcg else 0.0,
    }


def exact_match(prediction: str, reference: str) -> float:
    return float(prediction.strip().casefold() == reference.strip().casefold())


def token_f1(prediction: str, reference: str) -> float:
    """Simple whitespace-token F1; not a semantic similarity metric."""
    predicted = prediction.casefold().split()
    expected = reference.casefold().split()

    if not predicted or not expected:
        return float(predicted == expected)

    common = Counter(predicted) & Counter(expected)
    overlap = sum(common.values())

    if overlap == 0:
        return 0.0

    precision = overlap / len(predicted)
    recall = overlap / len(expected)
    return round(2 * precision * recall / (precision + recall), 4)
