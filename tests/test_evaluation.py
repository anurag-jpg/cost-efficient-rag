
import json

import pytest

from evaluation.dataset import load_dataset
from evaluation.metrics import (
    classification_metrics,
    exact_match,
    retrieval_metrics,
    token_f1,
)


def test_load_valid_dataset(tmp_path):
    path = tmp_path / "data.jsonl"
    record = {
        "id": "claim-001",
        "claim": "Flash Attention reduces memory traffic.",
        "evidence": "Flash Attention uses tiling to minimize memory reads and writes.",
        "label": "supported",
        "source": "research_paper.pdf",
        "page": 4,
    }
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")

    assert len(load_dataset(path)) == 1


def test_invalid_json_reports_line(tmp_path):
    path = tmp_path / "bad.jsonl"

    valid_record = {
        "id": "claim-001",
        "claim": "Example claim",
        "evidence": "Example evidence",
        "label": "supported",
        "source": "research_paper.pdf",
        "page": 1,
    }

    path.write_text(
        json.dumps(valid_record) + "\n{invalid json}\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="line 2"):
        load_dataset(path)


def test_duplicate_ids_rejected(tmp_path):
    path = tmp_path / "duplicates.jsonl"
    record = {
        "id": "same",
        "claim": "Claim",
        "evidence": "Evidence",
        "label": "supported",
        "source": "paper.pdf",
        "page": 1,
    }
    path.write_text(
        json.dumps(record) + "\n" + json.dumps(record) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate id"):
        load_dataset(path)


def test_classification_metrics():
    result = classification_metrics(
        ["supported", "contradicted", "supported"],
        ["supported", "contradicted", "insufficient_evidence"],
    )

    assert result["examples"] == 3
    assert result["accuracy"] == pytest.approx(2 / 3, abs=0.0001)
    assert "macro_f1" in result
    assert "confusion_matrix" in result


def test_retrieval_metrics():
    result = retrieval_metrics(
        relevant_ids={"chunk-A", "chunk-C"},
        ranked_ids=["chunk-B", "chunk-C", "chunk-A"],
        k=3,
    )

    assert result["recall@3"] == 1.0
    assert result["hit_rate@3"] == 1.0
    assert result["reciprocal_rank"] == 0.5
    assert 0.0 < result["ndcg@3"] <= 1.0



def test_exact_match_and_token_f1():
    assert exact_match("Hello", "hello") == 1.0
    assert token_f1("the cat sat", "the cat slept") == pytest.approx(
        0.6667, abs=0.0001
    )



def test_mismatched_prediction_counts():
    with pytest.raises(ValueError, match="equal lengths"):
        classification_metrics(["supported"], [])
