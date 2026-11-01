
def check_unique_ids(records, id_field):
    """Find duplicate IDs within a collection of records."""
    seen = set()
    duplicates = []

    for record in records:
        record_id = record.get(id_field)

        if record_id in seen:
            duplicates.append(record_id)
        else:
            seen.add(record_id)

    return duplicates


def check_foreign_keys(
    applicants,
    assets,
    quotes,
    policies,
    decisions
):
    """Check relationships between generated datasets."""

    errors = []

    applicant_ids = {a["applicant_id"] for a in applicants}
    asset_ids = {a["asset_id"] for a in assets}
    quote_ids = {q["quote_id"] for q in quotes}
    product_ids = {q["product_id"] for q in quotes}
    policy_quote_ids = {p["quote_id"] for p in policies}

    for asset in assets:
        if asset["applicant_id"] not in applicant_ids:
            errors.append(
                f"Asset {asset['asset_id']} has an unknown applicant."
            )

    for quote in quotes:
        if quote["applicant_id"] not in applicant_ids:
            errors.append(
                f"Quote {quote['quote_id']} has an unknown applicant."
            )

        if quote["asset_id"] not in asset_ids:
            errors.append(
                f"Quote {quote['quote_id']} has an unknown asset."
            )

    for policy in policies:
        if policy["quote_id"] not in quote_ids:
            errors.append(
                f"Policy {policy['policy_id']} has an unknown quote."
            )

    for decision in decisions:
        if decision["quote_id"] not in quote_ids:
            errors.append(
                f"Decision {decision['decision_id']} has an unknown quote."
            )

    # Check duplicate IDs.
    collections = [
        (applicants, "applicant_id"),
        (assets, "asset_id"),
        (quotes, "quote_id"),
        (policies, "policy_id"),
        (decisions, "decision_id"),
    ]

    for records, field in collections:
        duplicates = check_unique_ids(records, field)

        for duplicate in duplicates:
            errors.append(f"Duplicate {field}: {duplicate}")

    # One policy per quote in this initial data model.
   
    # Check that quotes are not reused by multiple policies,
    # except for the two intentionally injected policy anomalies.
    quote_policy_counts = {}

    for policy in policies:
        quote_id = policy["quote_id"]
        quote_policy_counts.setdefault(quote_id, []).append(policy)

    for quote_id, related_policies in quote_policy_counts.items():
        if len(related_policies) <= 1:
            continue

        is_expected_anomaly = any(
            policy["policy_id"].endswith("-EDGE-001")
            or policy["policy_id"].endswith("-OVERLAP-EDGE-001")
            for policy in related_policies
        )

        if not is_expected_anomaly:
            errors.append(
                f"Multiple policies reference quote {quote_id}."
            )

    return errors
