import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from validation.foreign_keys import (
    check_foreign_keys,
    check_unique_ids,
)


def test_duplicate_ids_are_detected():
    records = [
        {"applicant_id": "APP-001"},
        {"applicant_id": "APP-001"},
    ]

    assert check_unique_ids(records, "applicant_id") == ["APP-001"]


def test_valid_relationships_have_no_errors():
    applicants = [{"applicant_id": "APP-001"}]

    assets = [{
        "asset_id": "AST-001",
        "applicant_id": "APP-001",
    }]

    quotes = [{
        "quote_id": "QTE-001",
        "applicant_id": "APP-001",
        "asset_id": "AST-001",
        "product_id": "PRD-001",
    }]

    policies = [{
        "policy_id": "POL-001",
        "quote_id": "QTE-001",
    }]

    decisions = [{
        "decision_id": "DEC-001",
        "quote_id": "QTE-001",
    }]

    errors = check_foreign_keys(
        applicants, assets, quotes, policies, decisions
    )

    assert errors == []
