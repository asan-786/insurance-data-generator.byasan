 
import csv
import json
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from generator.edge_case_generator import (
    inject_policy_without_acceptance,
    inject_endorsement_limit_violation,
    inject_renewal_for_cancelled_policy,
    inject_overlapping_policy,
)  
from generator.anomaly_generator import inject_anomalies
from generator.applicants_assets import generate_applicants_assets
from generator.master_data import load_products
from generator.policy_lifecycle import generate_policies
from generator.quote_engine import generate_quotes
from generator.underwriting import evaluate_quotes


SEED = 2026
APPLICANT_COUNT = 3000
QUOTE_COUNT = 4000
POLICY_COUNT = 2000
RENEWAL_COUNT = 1200

OUTPUT_DIR = PROJECT_ROOT / "output"


def save_csv(filename, records):
    """Save a list of dictionaries as a CSV file."""
    if not records:
        print(f"Skipping {filename}: no records.")
        return

    path = OUTPUT_DIR / filename

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(records[0].keys())
        )
        writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} records to {path}")


def generate_renewals(
    policies,
    target_count=RENEWAL_COUNT,
    seed=SEED
):
    """Generate reproducible renewal records linked to active policies."""
    rng = random.Random(seed)

    eligible = [
        policy for policy in policies
        if policy["status"] == "ACTIVE"
    ]

    if len(eligible) < target_count:
        raise ValueError(
            f"Need {target_count} eligible policies for renewals, "
            f"but only {len(eligible)} are available."
        )

    rng.shuffle(eligible)
    renewals = []

    for policy in eligible[:target_count]:
        renewal_year = int(policy["end_date"][:4])

        renewals.append({
            "renewal_id": (
                f"REN-{policy['policy_id']}-{renewal_year}"
            ),
            "policy_id": policy["policy_id"],
            "renewal_year": renewal_year,
            "offered_premium": round(
                policy["premium"] * rng.uniform(1.02, 1.10),
                2
            ),
            "status": rng.choices(
                ["OFFERED", "ACCEPTED", "DECLINED"],
                weights=[20, 60, 20],
                k=1
            )[0],
        })

    return renewals


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating full synthetic insurance dataset...")

    # 1. Generate applicants and assets.
    applicants, assets = generate_applicants_assets(
        count=APPLICANT_COUNT,
        seed=SEED
    )

    # 2. Load insurance products.
    products = load_products()

    # 3. Generate quotes.
    quotes = generate_quotes(
        applicants=applicants,
        assets=assets,
        products=products,
        count=QUOTE_COUNT,
        seed=SEED
    )

    quotes, decisions = evaluate_quotes(quotes, products)

# Inject controlled anomalies after underwriting evaluation.
    quotes, ground_truth = inject_anomalies(
    quotes,
    seed=SEED,
    anomaly_rate=0.02
)

    print(f"Anomalies injected: {len(ground_truth)}")

    approved_quotes = [
        quote for quote in quotes
        if quote["status"] == "APPROVED"
    ]

    unique_combinations = {
        (quote["asset_id"], quote["product_id"])
        for quote in approved_quotes
    }

    print(f"Applicants generated: {len(applicants)}")
    print(f"Assets generated: {len(assets)}")
    print(f"Quotes generated: {len(quotes)}")
    print(f"Approved quotes: {len(approved_quotes)}")
    print(
        "Unique approved asset/product combinations: "
        f"{len(unique_combinations)}"
    )

    # 5. Generate policies from approved quotes.
    policies = generate_policies(
        quotes,
        seed=SEED,
        target_count=POLICY_COUNT
    )

   
    from generator.edge_case_generator import inject_policy_without_acceptance

# Inject one intentionally invalid policy for validation testing.
    edge_policy, edge_label = inject_policy_without_acceptance(policies)
    policies.append(edge_policy)
    ground_truth.append(edge_label)
    
    
    
# Select the policy that will be used for the cancelled-policy anomaly.
    cancel_policy = next(
      policy for policy in policies
      if policy.get("status") == "ACTIVE"
      and not policy["policy_id"].endswith("-EDGE-001")
      and not policy["policy_id"].endswith("-OVERLAP-EDGE-001")
)

    cancelled_policy_id = cancel_policy["policy_id"]

    

# Generate an endorsement that exceeds the product limit.
    product_by_id = {
    product["product_id"]: product
    for product in products
}

    valid_policy = next(
    (
        policy for policy in policies
        if policy.get("status") == "ACTIVE"
        and not policy["policy_id"].endswith("-EDGE-001")
        and not policy["policy_id"].endswith("-OVERLAP-EDGE-001")
        and policy["policy_id"] != cancelled_policy_id
    ),
    None,
)

    if valid_policy is None:
     raise ValueError("No suitable active policy found for endorsement.")

    matching_product = product_by_id[valid_policy["product_id"]]

    edge_endorsement, endorsement_label = (
    inject_endorsement_limit_violation(
        valid_policy,
        matching_product,
    )
)

    ground_truth.append(endorsement_label)
    endorsements = [edge_endorsement]


   
    # 6. Generate renewals for active policies.
    renewals = generate_renewals(
        policies,
        target_count=RENEWAL_COUNT,
        seed=SEED
    )
    
    
     

# Inject a renewal linked to an actually cancelled policy.

    valid_policy = next(
     policy for policy in policies
      if not policy["policy_id"].endswith("-EDGE-001")
      and not policy["policy_id"].endswith("-OVERLAP-EDGE-001")
      and policy["status"] == "ACTIVE"
     if policy["policy_id"] == cancelled_policy_id
)


    cancelled_policy, edge_renewal, renewal_label = (
    inject_renewal_for_cancelled_policy(
        valid_policy,
        int(valid_policy["end_date"][:4]) + 1,
    )
)

# Replace the original policy with its cancelled version.
    for index, policy in enumerate(policies):
     if policy["policy_id"] == cancelled_policy["policy_id"]:
        policies[index] = cancelled_policy
        break

    renewals.append(edge_renewal)
    ground_truth.append(renewal_label)
    
    
    # Inject overlapping policy periods.
    edge_overlap_policy, overlap_label = inject_overlapping_policy(policies)

    policies.append(edge_overlap_policy)
    ground_truth.append(overlap_label)

    print("Injected overlapping policy period edge case.")




    print(f"Policies issued: {len(policies)}")
    print(f"Renewals generated: {len(renewals)}")

    # 7. Save datasets.
    save_csv("applicants.csv", applicants)
    save_csv("assets.csv", assets)
    save_csv("quotes.csv", quotes)
    save_csv("underwriting_decisions.csv", decisions)
    save_csv("policies.csv", policies)
    save_csv("renewals.csv", renewals)
    save_csv("ground_truth.csv", ground_truth)
    save_csv("endorsements.csv", [edge_endorsement])

    # 8. Save generation summary.
    summary = {
        "seed": SEED,
        "applicants": len(applicants),
        "assets": len(assets),
        "quotes": len(quotes),
        "underwriting_decisions": len(decisions),
        "products": len(products),
        "policies": len(policies),
        "renewals": len(renewals),
    }

    summary_path = OUTPUT_DIR / "generation_summary.json"

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print("\nGeneration summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

    
