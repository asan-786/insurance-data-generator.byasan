
import random
from datetime import date, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from id_generator import IDGenerator


def issue_policy(
    quote,
    accepted,
    payment_completed,
    start_date,
    term_days=365
):
    """
    Issue a policy only when the quote is approved,
    accepted by the customer, and payment is completed.
    """

    if quote["status"] != "APPROVED":
        raise ValueError(
            "Policy cannot be issued: quote is not approved."
        )

    if not accepted:
        raise ValueError(
            "Policy cannot be issued: customer has not accepted."
        )

    if not payment_completed:
        raise ValueError(
            "Policy cannot be issued: payment is incomplete."
        )

    if term_days <= 0:
        raise ValueError("Policy term must be positive.")

    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)

    end_date = start_date + timedelta(days=term_days)

    return {
        "quote_id": quote["quote_id"],
        "accepted": accepted,
        "payment_completed": payment_completed,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "status": "ACTIVE",
        "coverage": quote["requested_coverage"],
    }


def generate_policies(quotes, seed=2026, target_count=2000):
    """Generate a controlled number of valid policies when possible."""

    rng = random.Random(seed)
    ids = IDGenerator(year=2026)
    policies = []
    used_asset_products = set()

    # Keep one approved quote per asset/product combination.
    eligible_quotes = []
    for quote in quotes:
        if quote["status"] != "APPROVED":
            continue

        key = (quote["asset_id"], quote["product_id"])
        if key in used_asset_products:
            continue

        used_asset_products.add(key)
        eligible_quotes.append(quote)

    # Shuffle deterministically so selection is reproducible.
    rng.shuffle(eligible_quotes)

    if len(eligible_quotes) < target_count:
        raise ValueError(
            f"Cannot generate {target_count} policies: "
            f"only {len(eligible_quotes)} unique approved "
            "asset/product combinations are available."
        )

    selected_quotes = eligible_quotes[:target_count]

    for quote in selected_quotes:
        # These policies represent successful acceptance and payment.
        accepted = True
        payment_completed = True

        policy = issue_policy(
            quote=quote,
            accepted=accepted,
            payment_completed=payment_completed,
            start_date=date(2026, 1, 3),
            term_days=365,
        )

        policy["policy_id"] = ids.generate("policy")
        policy["applicant_id"] = quote["applicant_id"]
        policy["asset_id"] = quote["asset_id"]
        policy["product_id"] = quote["product_id"]
        policy["premium"] = quote["premium"]

        policies.append(policy)

    return policies



# def generate_policies(quotes, seed=2026):
#     rng = random.Random(seed)
#     ids = IDGenerator(year=2026)
#     policies = []
#     used_asset_products = set()

#     for quote in quotes:
#         if quote["status"] != "APPROVED":
#             continue

#         key = (quote["asset_id"], quote["product_id"])
#         if key in used_asset_products:
#             continue

#         # Keep your existing acceptance and payment checks here.
#         accepted = rng.random() < 0.80
#         if not accepted:
#             continue

#         payment_completed = rng.random() < 0.95
#         if not payment_completed:
#             continue

#         # Keep your existing issue_policy() call and field assignments here.
#         # After creating the policy:
#         policies.append(policy)
#         used_asset_products.add(key)

#     return policies


def create_endorsement(
    policy,
    new_coverage,
    product,
    effective_date
):
    """Record a coverage change without overwriting policy history."""

    if policy["status"] != "ACTIVE":
        raise ValueError(
            "Endorsement requires an active policy."
        )

    if new_coverage <= 0:
        raise ValueError("New coverage must be positive.")

    if new_coverage > product["max_coverage"]:
        raise ValueError(
            "Endorsement exceeds the product coverage limit."
        )

    old_coverage = policy.get("current_coverage")

    if old_coverage is None:
        old_coverage = policy["coverage"]

    if isinstance(effective_date, str):
        effective_date = date.fromisoformat(effective_date)

    start_date = date.fromisoformat(policy["start_date"])
    end_date = date.fromisoformat(policy["end_date"])

    if not start_date <= effective_date <= end_date:
        raise ValueError(
            "Endorsement date must fall within the policy period."
        )

    endorsement = {
        "endorsement_id": (
            f"END-{policy['policy_id']}-001"
        ),
        "policy_id": policy["policy_id"],
        "previous_coverage": old_coverage,
        "new_coverage": new_coverage,
        "effective_date": effective_date.isoformat(),
        "status": "APPLIED",
    }

    # Preserve original coverage and update current coverage.
    policy.setdefault("coverage", old_coverage)
    policy["current_coverage"] = new_coverage

    return endorsement


def create_renewal(policy, renewal_year, offered_premium):
    """Create a renewal offer for an eligible policy."""

    if policy["status"] == "CANCELLED":
        raise ValueError(
            "Cancelled policies cannot be renewed."
        )

    if policy["status"] != "ACTIVE":
        raise ValueError(
            "Only active policies can receive renewal offers."
        )

    if offered_premium <= 0:
        raise ValueError("Renewal premium must be positive.")

    policy_end = date.fromisoformat(policy["end_date"])

    if date(renewal_year, 1, 1) <= policy_end:
     raise ValueError(
        "Renewal date must be after the current policy end date."
    )

    return {
        "renewal_id": (
            f"REN-{policy['policy_id']}-{renewal_year}"
        ),
        "policy_id": policy["policy_id"],
        "renewal_year": renewal_year,
        "offered_premium": round(offered_premium, 2),
        "status": "OFFERED",
    }


def cancel_policy(policy, cancellation_date):
    """Cancel an active policy and preserve its original dates."""

    if policy["status"] != "ACTIVE":
        raise ValueError(
            "Only active policies can be cancelled."
        )

    if isinstance(cancellation_date, str):
        cancellation_date = date.fromisoformat(
            cancellation_date
        )

    start_date = date.fromisoformat(policy["start_date"])
    end_date = date.fromisoformat(policy["end_date"])

    if not start_date <= cancellation_date <= end_date:
        raise ValueError(
            "Cancellation date must fall within the policy period."
        )

    policy["status"] = "CANCELLED"
    policy["cancellation_date"] = cancellation_date.isoformat()

    return policy



if __name__ == "__main__":
    from master_data import load_products
    from applicants_assets import generate_applicants_assets
    from quote_engine import generate_quotes
    from underwriting import evaluate_quotes

    applicants, assets = generate_applicants_assets(
        count=100,
        seed=2026
    )

    products = load_products()

    quotes = generate_quotes(
        applicants=applicants,
        assets=assets,
        products=products,
        count=150,
        seed=2026
    )

    quotes, decisions = evaluate_quotes(quotes, products)

    policies = generate_policies(quotes, seed=2026)

    print(f"Quotes generated: {len(quotes)}")
    print(f"Underwriting decisions: {len(decisions)}")
    print(f"Policies issued: {len(policies)}")

    if policies:
        print("\nFirst policy:")
        print(policies[0])

    # Test that unaccepted quotes cannot be issued.
    approved_quote = next(
        (q for q in quotes if q["status"] == "APPROVED"),
        None
    )

    if approved_quote:
        try:
            issue_policy(
                quote=approved_quote,
                accepted=False,
                payment_completed=True,
                start_date=date(2026, 1, 3)
            )
        except ValueError as error:
            print("\nExpected validation:", error)
            
        
    # Test endorsement and renewal rules.
    if policies:
        test_policy = policies[0]

        test_product = next(
            p for p in products
            if p["product_id"] == test_policy["product_id"]
        )

        print("\n--- Endorsement test ---")

        endorsement = create_endorsement(
            policy=test_policy,
            new_coverage=min(
                test_policy["coverage"] + 10000,
                test_product["max_coverage"]
            ),
            product=test_product,
            effective_date="2026-06-01"
        )

        print(endorsement)

        print("\n--- Renewal test ---")

        renewal = create_renewal(
            policy=test_policy,
            renewal_year=2028,
            offered_premium=test_policy["premium"] * 1.05
        )

        # Simulate a customer declining the renewal.
        renewal["status"] = "DECLINED"
        print(renewal)

        print("\n--- Cancellation test ---")

        cancel_policy(
            test_policy,
            cancellation_date="2026-07-01"
        )

        print("Policy status:", test_policy["status"])

        try:
            create_renewal(
                policy=test_policy,
                renewal_year=2027,
                offered_premium=test_policy["premium"]
            )
        except ValueError as error:
            print("Expected validation:", error)
