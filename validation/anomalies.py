
import csv
from pathlib import Path


def validate_anomalies(output_dir="output"):
    output_path = Path(output_dir)

    with open(
        output_path / "quotes.csv",
        newline="",
        encoding="utf-8"
    ) as file:
        quotes = {
            row["quote_id"]: row
            for row in csv.DictReader(file)
        }

    with open(
        output_path / "ground_truth.csv",
        newline="",
        encoding="utf-8"
    ) as file:
        labels = list(csv.DictReader(file))

    errors = []

    for label in labels:
        quote_id = label["entity_id"]
        quote = quotes.get(quote_id)

        if quote is None:
            errors.append(f"Missing quote: {quote_id}")
            continue

        actual_premium = float(quote["premium"])
        expected_premium = float(label["anomalous_value"])

        if abs(actual_premium - expected_premium) > 0.01:
            errors.append(
                f"Premium mismatch for {quote_id}: "
                f"expected {expected_premium}, "
                f"found {actual_premium}"
            )

        if label["issue_type"] != "PREMIUM_ANOMALY":
            errors.append(f"Unexpected issue type: {quote_id}")

        if label["is_anomaly"].lower() != "true":
            errors.append(f"Invalid anomaly label: {quote_id}")

    return {
        "total_labels": len(labels),
        "errors": errors,
        "valid": len(errors) == 0,
    }


if __name__ == "__main__":
    result = validate_anomalies()
    print(result)
