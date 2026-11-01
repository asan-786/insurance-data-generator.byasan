
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from id_generator import IDGenerator


def evaluate_quote(quote, product):
    """
    Evaluate a quote using transparent underwriting rules.
    Returns the decision and its explanation.
    """

    reasons = []
    risk_score = 0

    # Rule 1: Validate requested coverage.
    if quote["requested_coverage"] <= 0:
        return "DECLINED", "INVALID_COVERAGE", 0

    if quote["requested_coverage"] > product["max_coverage"]:
        return "DECLINED", "COVERAGE_EXCEEDS_PRODUCT_LIMIT", 0

    # Rule 2: Missing risk information requires manual review.
    if not quote.get("claim_history"):
        return "REFERRED", "MISSING_CLAIM_HISTORY", 0

    if (
        quote.get("product_line") == "MOTOR"
        and not quote.get("vehicle_age_category")
    ):
        return "REFERRED", "MISSING_VEHICLE_AGE", 0

    # Rule 3: Calculate an explainable risk score.
    claim_points = {
        "no_claims": 0,
        "one_claim": 1,
        "multiple_claims": 2,
    }

    age_points = {
        "new": 0,
        "medium": 1,
        "old": 2,
    }

    claim_history = quote["claim_history"]

    if claim_history not in claim_points:
        return "REFERRED", "UNKNOWN_CLAIM_HISTORY", 0

    risk_score += claim_points[claim_history]

    if quote.get("product_line") == "MOTOR":
        vehicle_age = quote["vehicle_age_category"]

        if vehicle_age not in age_points:
            return "REFERRED", "UNKNOWN_VEHICLE_AGE", risk_score

        risk_score += age_points[vehicle_age]

    # Rule 4: Refer high-risk quotes for manual underwriting.
    if risk_score >= 3:
        reasons.append("HIGH_RISK_SCORE")
        return "REFERRED", ";".join(reasons), risk_score

    return "APPROVED", "WITHIN_AUTOMATED_RISK_LIMIT", risk_score


def evaluate_quotes(quotes, products):
    """Evaluate all quotes and return updated quotes and decisions."""

    product_by_id = {
        product["product_id"]: product
        for product in products
    }

    ids = IDGenerator(year=2026)
    decisions = []

    for quote in quotes:
        product = product_by_id.get(quote["product_id"])

        if product is None:
            raise ValueError(
                f"Product not found for quote {quote['quote_id']}"
            )

        decision, reason, risk_score = evaluate_quote(quote, product)

        # Update the quote's current status.
        quote["status"] = decision

        decisions.append({
            "decision_id": ids.generate("decision"),
            "quote_id": quote["quote_id"],
            "decision": decision,
            "reason_code": reason,
            "risk_score": risk_score,
            "decision_at": datetime(
                2026, 1, 2, 10, 0, 0
            ).isoformat(),
        })
        
        

    return quotes, decisions
  
     
if __name__ == "__main__":
    from master_data import load_products
    from applicants_assets import generate_applicants_assets
    from quote_engine import generate_quotes

    # Step 1: Generate sample applicants and assets
    applicants, assets = generate_applicants_assets(
        count=10,
        seed=2026
    )

    # Step 2: Load product configuration
    products = load_products()

    # Step 3: Generate sample quotes
    quotes = generate_quotes(
        applicants=applicants,
        assets=assets,
        products=products,
        count=15,
        seed=2026
    )

    # Step 4: Evaluate the quotes
    updated_quotes, decisions = evaluate_quotes(
        quotes,
        products
    )

    # Step 5: Display results
    print(f"Quotes evaluated: {len(updated_quotes)}")
    print(f"Decisions created: {len(decisions)}")

    for decision in decisions[:5]:
        print(
            decision["quote_id"],
            decision["decision"],
            decision["reason_code"],
            "Risk score:",
            decision["risk_score"]
        )
