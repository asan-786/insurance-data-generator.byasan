
import csv
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from generator.master_data import load_products
from validation.foreign_keys import check_foreign_keys
from validation.business_rules import (
     validate_premiums,
    validate_policies,
    validate_endorsements,
    validate_renewals,
    validate_overlapping_policies,
)


OUTPUT_DIR = PROJECT_ROOT / "output"


# def load_csv(filename):
#     """Load generated records from an output CSV file."""
#     path = OUTPUT_DIR / filename

#     with open(path, "r", newline="", encoding="utf-8") as file:
#         return list(csv.DictReader(file))


def load_csv(filename):
    """Load generated records from CSV and convert numeric values."""
    path = OUTPUT_DIR / filename
    

    with open(path, "r", newline="", encoding="utf-8") as file:
     records = list(csv.DictReader(file))
    numeric_fields = {
        "premium",
        "coverage_amount",
        "offered_premium",
        "renewal_year",
        "risk_score",
        "asset_value",
        "max_coverage",
        "base_premium",
        "previous_coverage",
        "new_coverage",
    }
    
    boolean_fields = {
    "customer_accepted",
    "payment_complete",
    "payment_completed",
    "accepted",
    "payment_received",
}

    for record in records:
        for field in numeric_fields:
            if field in record and record[field] not in ("", None):
                record[field] = float(record[field])
                
         # Convert boolean fields.
        for field in boolean_fields:
            if field in record and record[field] != "":
                value = record[field].strip().lower()

                if value in ("true", "1", "yes"):
                    record[field] = True
                elif value in ("false", "0", "no"):
                    record[field] = False        

    return records



def load_premium_factors():
    path = PROJECT_ROOT / "config" / "premium_factors.json"

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("Loading full generated insurance dataset...")

    applicants = load_csv("applicants.csv")
    assets = load_csv("assets.csv")
    quotes = load_csv("quotes.csv")
    decisions = load_csv("underwriting_decisions.csv")
    policies = load_csv("policies.csv")
    endorsements = load_csv("endorsements.csv")
    renewals = load_csv("renewals.csv")
    ground_truth = load_csv("ground_truth.csv")

    products = load_products()

    print(f"Applicants: {len(applicants)}")
    print(f"Assets: {len(assets)}")
    print(f"Quotes: {len(quotes)}")
    print(f"Decisions: {len(decisions)}")
    print(f"Policies: {len(policies)}")
    print(f"Renewals: {len(renewals)}")

    print("\nRunning validation checks...")

#     checks = {
#         "foreign_keys": check_foreign_keys(
#             applicants, assets, quotes, policies, decisions
#         ),
#        "premiums": validate_premiums(
#          quotes,
#          products,
#          load_premium_factors(),
#         ground_truth,
# ),
#         "policies": validate_policies(policies, quotes),
#         "overlapping_policies": validate_overlapping_policies(policies),
#     }


    checks = {
        "foreign_keys": check_foreign_keys(
            applicants, assets, quotes, policies, decisions
        ),
        "premiums": validate_premiums(
            quotes,
            products,
            load_premium_factors(),
            ground_truth,
        ),
          "policies": validate_policies(policies, quotes),
        "endorsements": validate_endorsements(
            endorsements, policies, products
        ),
        "renewals": validate_renewals(renewals, policies),
        "overlapping_policies": validate_overlapping_policies(policies),
    }

    
    expected_labels = {
        (row["entity_id"], row["issue_type"])
        for row in ground_truth
        if str(row.get("is_anomaly", "")).strip().lower()
        in ("true", "1", "yes")
    }

    expected_findings = []
    unexpected_findings = []

    for check_name, errors in checks.items():
        for error in errors:
            expected = False

          
    if check_name == "policies":
     expected = any(
    issue_type in allowed_types
    and entity_id in error
    and (
        check_name != "endorsements"
        or "new coverage exceeds product limit" in error.lower()
    )
    for entity_id, issue_type in expected_labels
)

    elif check_name == "endorsements":
     expected = any(
        issue_type == "ENDORSEMENT_EXCEEDS_PRODUCT_LIMIT"
        and entity_id in error
        for entity_id, issue_type in expected_labels
    )

    elif check_name == "renewals":
     expected = any(
        issue_type == "RENEWAL_FOR_CANCELLED_POLICY"
        and entity_id in error
        for entity_id, issue_type in expected_labels
    )

    elif check_name == "overlapping_policies":
     expected = any(
        issue_type == "OVERLAPPING_POLICY_PERIODS"
        and entity_id in error
        for entity_id, issue_type in expected_labels
    )


    finding = {
                "check": check_name,
                "message": error,
                "classification": (
                    "EXPECTED_ANOMALY" if expected else "UNEXPECTED_ERROR"
                ),
            }# Map intentionally injected anomalies to their entity IDs.

   
    # Map intentionally injected anomalies to their entity IDs.
    expected_labels = {
        (row["entity_id"], row["issue_type"])
        for row in ground_truth
        if str(row.get("is_anomaly", "")).strip().lower()
        in ("true", "1", "yes")
    }

    matching_types = {
        "policies": {"POLICY_WITHOUT_ACCEPTANCE"},
        "endorsements": {"ENDORSEMENT_EXCEEDS_PRODUCT_LIMIT"},
        "renewals": {"RENEWAL_FOR_CANCELLED_POLICY"},
        "overlapping_policies": {"OVERLAPPING_POLICY_PERIODS"},
    }

    expected_findings = []
    unexpected_findings = []

    for check_name, errors in checks.items():
        for error in errors:
            allowed_types = matching_types.get(check_name, set())

            expected = any(
                issue_type in allowed_types
                and entity_id in error
                and (
                    check_name != "endorsements"
                    or "new coverage exceeds product limit" in error.lower()
                )
                for entity_id, issue_type in expected_labels
            )

            finding = {
                "check": check_name,
                "message": error,
                "classification": (
                    "EXPECTED_ANOMALY" if expected else "UNEXPECTED_ERROR"
                ),
            }

            if expected:
                expected_findings.append(finding)
            else:
                unexpected_findings.append(finding)

    print("\nValidation findings:")
    print(f"Expected anomalies detected: {len(expected_findings)}")
    print(f"Unexpected errors: {len(unexpected_findings)}")

    for finding in expected_findings:
        print(
            f"  [EXPECTED] {finding['check']}: "
            f"{finding['message']}"
        )

    for finding in unexpected_findings:
        print(
            f"  [UNEXPECTED] {finding['check']}: "
            f"{finding['message']}"
        )

    total_errors = len(unexpected_findings)

    report = {
        "seed": 2026,
        "record_counts": {
            "applicants": len(applicants),
            "assets": len(assets),
            "quotes": len(quotes),
            "decisions": len(decisions),
            "policies": len(policies),
            "endorsements": len(endorsements),
            "renewals": len(renewals),
            "products": len(products),
        },
        "anomaly_summary": {
            issue_type: sum(
                1
                for row in ground_truth
                if row.get("issue_type") == issue_type
                and str(row.get("is_anomaly", "")).strip().lower()
                in ("true", "1", "yes")
            )
            for issue_type in {
                "PREMIUM_ANOMALY",
                "POLICY_WITHOUT_ACCEPTANCE",
                "ENDORSEMENT_EXCEEDS_PRODUCT_LIMIT",
                "RENEWAL_FOR_CANCELLED_POLICY",
                "OVERLAPPING_POLICY_PERIODS",
            }
        },
        "expected_findings": expected_findings,
        "unexpected_findings": unexpected_findings,
        "checks": checks,
        "total_errors": total_errors,
        "result": "PASS" if total_errors == 0 else "FAIL",
    }


    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT_DIR / "validation_report.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f"\nOverall result: {report['result']}")
    print(f"Total validation errors: {total_errors}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
