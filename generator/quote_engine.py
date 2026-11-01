
import random
from pathlib import Path
import sys

# Allow imports from the generator folder
sys.path.insert(0, str(Path(__file__).resolve().parent))

from id_generator import IDGenerator
from applicants_assets import generate_applicants_assets
from master_data import load_products


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FACTORS_FILE = PROJECT_ROOT / "config" / "premium_factors.json"


def load_premium_factors():
    import json

    with open(FACTORS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_premium(base_premium, vehicle_factor, claims_factor):
    """Calculate the premium using the configured factors."""
    return round(
        base_premium * vehicle_factor * claims_factor, 2
    )


def generate_quotes(
    applicants,
    assets,
    products,
    count=15,
    seed=2026
):
    """Generate quotes linked to existing applicants, assets and products."""
    rng = random.Random(seed)
    ids = IDGenerator(year=2026)
    factors = load_premium_factors()

    if not applicants or not assets or not products:
        raise ValueError(
            "Applicants, assets and products must not be empty."
        )

    applicant_ids = {a["applicant_id"] for a in applicants}
    asset_by_id = {a["asset_id"]: a for a in assets}

    # Group products by product line
    product_by_line = {
        p["product_line"]: p for p in products
    }

    # Group assets by their owner and type
    eligible_assets = [
        a for a in assets
        if a["applicant_id"] in applicant_ids
        and a["asset_type"] in product_by_line
    ]

    if not eligible_assets:
        raise ValueError("No assets match the configured products.")

    claims_factors = factors["claim_history_factor"]
    vehicle_factors = factors["vehicle_age_factor"]

    claim_categories = list(claims_factors.keys())
    vehicle_categories = list(vehicle_factors.keys())

    quotes = []

    for _ in range(count):
        asset = rng.choice(eligible_assets)
        applicant_id = asset["applicant_id"]
        product = product_by_line[asset["asset_type"]]

        max_coverage = min(
            product["max_coverage"],
            asset["asset_value"]
        )

        requested_coverage = round(
            rng.uniform(min(100000, max_coverage), max_coverage),
            2
        )

        claim_history = rng.choice(claim_categories)
        claims_factor = claims_factors[claim_history]

        # Vehicle-age pricing applies only to motor insurance.
        if product["product_line"] == "MOTOR":
            vehicle_age_category = rng.choice(vehicle_categories)
            vehicle_factor = vehicle_factors[vehicle_age_category]
        else:
            vehicle_age_category = "not_applicable"
            vehicle_factor = 1.0

        premium = calculate_premium(
            product["base_premium"],
            vehicle_factor,
            claims_factor
        )

        quote = {
            "quote_id": ids.generate("quote"),
            "applicant_id": applicant_id,
            "asset_id": asset["asset_id"],
            "product_id": product["product_id"],
            "product_line": product["product_line"],
            "requested_coverage": requested_coverage,
            "base_premium": product["base_premium"],
            "vehicle_age_category": vehicle_age_category,
            "vehicle_factor": vehicle_factor,
            "claim_history": claim_history,
            "claims_factor": claims_factor,
            "premium": premium,
            "status": "SUBMITTED",
            "created_at": "2026-01-01T10:00:00"
        }

        quotes.append(quote)

    return quotes


if __name__ == "__main__":
    applicants, assets = generate_applicants_assets(
        count=10,
        seed=2026
    )

    products = load_products()

    quotes = generate_quotes(
        applicants=applicants,
        assets=assets,
        products=products,
        count=15,
        seed=2026
    )

    print(f"Generated {len(quotes)} quotes")
    print("\nFirst quote:")

    for key, value in quotes[0].items():
        print(f"{key}: {value}")
