
from collections import Counter

from evaluation.dataset import load_dataset


def main():
    path = "data/eval/claim_citations.jsonl"
    records = load_dataset(path)

    print(f"Total records: {len(records)}")
    print("Label distribution:")

    for label, count in sorted(
        Counter(record["label"] for record in records).items()
    ):
        print(f"  {label}: {count}")

    print("\nRecords to review:")
    for record in records:
        print(
            f"{record['id']} | "
            f"page={record['page']} | "
            f"label={record['label']}"
        )

    print("\nDataset format is valid.")
    print("Manual PDF verification is still required.")


if __name__ == "__main__":
    main()
