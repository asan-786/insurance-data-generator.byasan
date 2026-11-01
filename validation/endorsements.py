
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output"
PRODUCTS_FILE = ROOT / "config" / "products.json"


def validate_endorsements():
    with open(PRODUCTS_FILE, encoding="utf-8") as file:
        products = json.load(file)["products"]

    product_by_id = {
        product["product_id"]: product
        for product in products
    }

    with open(OUTPUT / "policies.csv", newline="", encoding="utf-8") as file:
        policies = list(csv.DictReader(file))

    with open(OUTPUT / "endorsements.csv", newline="", encoding="utf-8") as file:
        endorsements = list(csv.DictReader(file))

    policy_by_id = {
        policy["policy_id"]: policy
        for policy in policies
    }

    errors = []

    for endorsement in endorsements:
        policy = policy_by_id.get(endorsement["policy_id"])

        if policy is None:
            errors.append(
                f"Unknown policy: {endorsement['policy_id']}"
            )
            continue

        product = product_by_id.get(policy["product_id"])

        if product is None:
            errors.append(
                f"Unknown product: {policy['product_id']}"
            )
            continue

        new_coverage = float(endorsement["new_coverage"])
        max_coverage = float(product["max_coverage"])

        if new_coverage > max_coverage:
            print(
                f"Detected intended anomaly: "
                f"{endorsement['endorsement_id']} exceeds "
                f"the product limit by "
                f"{new_coverage - max_coverage:.2f}"
            )

    print("Validation errors:", errors)
    return errors


if __name__ == "__main__":
    validate_endorsements()
