
from validation.business_rules import (
    validate_premiums,
    validate_policies,
    validate_renewals,
    validate_overlapping_policies,
)


def test_valid_premium():
    products = [{
        "product_id": "PRD-001",
        "product_line": "MOTOR",
        "base_premium": 5000,
    }]

    factors = {
        "vehicle_age_factor": {
            "new": 1.0,
            "medium": 1.2,
            "old": 1.5,
        },
        "claim_history_factor": {
            "no_claims": 1.0,
            "one_claim": 1.1,
            "multiple_claims": 1.4,
        },
    }

    quotes = [{
        "quote_id": "QTE-001",
        "product_id": "PRD-001",
        "product_line": "MOTOR",
        "vehicle_age_category": "new",
        "claim_history": "no_claims",
        "premium": 5000,
    }]

    assert validate_premiums(quotes, products, factors) == []


def test_incorrect_premium_is_detected():
    products = [{
        "product_id": "PRD-001",
        "product_line": "MOTOR",
        "base_premium": 5000,
    }]

    factors = {
        "vehicle_age_factor": {"new": 1.0},
        "claim_history_factor": {"no_claims": 1.0},
    }

    quotes = [{
        "quote_id": "QTE-001",
        "product_id": "PRD-001",
        "product_line": "MOTOR",
        "vehicle_age_category": "new",
        "claim_history": "no_claims",
        "premium": 9999,
    }]

    errors = validate_premiums(quotes, products, factors)

    assert len(errors) == 1
    assert "incorrect premium" in errors[0]


def test_unaccepted_policy_is_detected():
    quotes = [{
        "quote_id": "QTE-001",
        "status": "APPROVED",
    }]

    policies = [{
        "policy_id": "POL-001",
        "quote_id": "QTE-001",
        "accepted": False,
        "payment_completed": True,
        "start_date": "2026-01-01",
        "end_date": "2027-01-01",
    }]

    errors = validate_policies(policies, quotes)

    assert any("acceptance is missing" in e for e in errors)


def test_cancelled_policy_renewal_is_detected():
    policies = [{
        "policy_id": "POL-001",
        "status": "CANCELLED",
    }]

    renewals = [{
        "renewal_id": "REN-001",
        "policy_id": "POL-001",
        "offered_premium": 5000,
    }]

    errors = validate_renewals(renewals, policies)

    assert any("cancelled policy" in e for e in errors)


def test_overlapping_policies_are_detected():
    policies = [
        {
            "policy_id": "POL-001",
            "asset_id": "AST-001",
            "product_id": "PRD-001",
            "start_date": "2026-01-01",
            "end_date": "2027-01-01",
            "status": "ACTIVE",
        },
        {
            "policy_id": "POL-002",
            "asset_id": "AST-001",
            "product_id": "PRD-001",
            "start_date": "2026-06-01",
            "end_date": "2027-06-01",
            "status": "ACTIVE",
        },
    ]

    errors = validate_overlapping_policies(policies)

    assert len(errors) == 1



import pytest
from datetime import date

from generator.policy_lifecycle import issue_policy


def test_policy_cannot_be_issued_without_acceptance():
    quote = {
        "quote_id": "QTE-001",
        "applicant_id": "APP-001",
        "asset_id": "AST-001",
        "product_id": "PRD-001",
        "premium": 5000,
        "status": "APPROVED",
    }

    with pytest.raises(ValueError):
        issue_policy(
            quote=quote,
            accepted=False,
            payment_completed=True,
            start_date=date(2026, 1, 1),
            term_days=365,
        )






from generator.policy_lifecycle import create_endorsement


def test_endorsement_cannot_exceed_product_limit():
    policy = {
        "policy_id": "POL-001",
        "status": "ACTIVE",
        "coverage": 500000,
        "current_coverage": 500000,
        "start_date": "2026-01-01",
        "end_date": "2027-01-01",
    }

    product = {
        "product_id": "PRD-001",
        "max_coverage": 1000000,
    }

    with pytest.raises(ValueError):
        create_endorsement(
            policy=policy,
            new_coverage=1500000,
            product=product,
            effective_date=date(2026, 6, 1),
        )
