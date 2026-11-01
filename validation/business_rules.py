
from datetime import date



def validate_premiums(quotes, products, premium_factors, ground_truth=None):
    """Validate premiums while distinguishing intentional anomalies."""

    errors = []
    detected_anomalies = []

    product_by_id = {
        product["product_id"]: product
        for product in products
    }

    # Identify quotes intentionally modified by the generator.
    anomaly_labels = {
        label["entity_id"]: label
        for label in (ground_truth or [])
        if label.get("issue_type") == "PREMIUM_ANOMALY"
    }

    for quote in quotes:
        quote_id = quote["quote_id"]
        product = product_by_id.get(quote["product_id"])

        if product is None:
            errors.append(f"{quote_id}: unknown product.")
            continue

        vehicle_category = quote.get("vehicle_age_category")
        claim_history = quote.get("claim_history")

        if claim_history not in premium_factors["claim_history_factor"]:
            errors.append(f"{quote_id}: invalid claim history.")
            continue

        expected_vehicle_factor = 1.0

        if quote["product_line"] == "MOTOR":
            vehicle_factors = premium_factors["vehicle_age_factor"]

            if vehicle_category not in vehicle_factors:
                errors.append(f"{quote_id}: invalid vehicle age category.")
                continue

            expected_vehicle_factor = vehicle_factors[vehicle_category]

        expected_claim_factor = premium_factors[
            "claim_history_factor"
        ][claim_history]

        expected_premium = round(
            product["base_premium"]
            * expected_vehicle_factor
            * expected_claim_factor,
            2,
        )

        actual_premium = float(quote["premium"])

        if abs(actual_premium - expected_premium) > 0.01:
            if quote_id in anomaly_labels:
                detected_anomalies.append(
                    f"{quote_id}: expected injected premium anomaly detected."
                )
            else:
                errors.append(
                    f"{quote_id}: incorrect premium; "
                    f"expected {expected_premium}, "
                    f"found {actual_premium}."
                )
        elif quote_id in anomaly_labels:
            errors.append(
                f"{quote_id}: labeled as a premium anomaly, "
                "but its premium matches the expected formula."
            )

    print(f"Expected premium anomalies detected: {len(detected_anomalies)}")

    return errors



def validate_policies(policies, quotes):
    """Check policy issuance requirements and lifecycle dates."""

    errors = []
    quote_by_id = {
        quote["quote_id"]: quote
        for quote in quotes
    }

    for policy in policies:
        policy_id = policy["policy_id"]
        quote = quote_by_id.get(policy["quote_id"])

        if quote is None:
            errors.append(
                f"{policy_id}: referenced quote does not exist."
            )
        elif quote["status"] != "APPROVED":
            errors.append(
                f"{policy_id}: policy quote is not approved."
            )

        if policy.get("accepted") is not True:
            errors.append(
                f"{policy_id}: customer acceptance is missing."
            )

        if policy.get("payment_completed") is not True:
            errors.append(
                f"{policy_id}: payment is incomplete."
            )

        try:
            start = date.fromisoformat(policy["start_date"])
            end = date.fromisoformat(policy["end_date"])

            if end <= start:
                errors.append(
                    f"{policy_id}: end date must be after start date."
                )
        except (ValueError, TypeError, KeyError):
            errors.append(
                f"{policy_id}: invalid or missing policy dates."
            )

    return errors


def validate_endorsements(endorsements, policies, products):
    """Check endorsement limits and coverage history."""

    errors = []

    policy_by_id = {
        policy["policy_id"]: policy
        for policy in policies
    }

    product_by_id = {
        product["product_id"]: product
        for product in products
    }

    for endorsement in endorsements:
        endorsement_id = endorsement["endorsement_id"]
        policy = policy_by_id.get(endorsement["policy_id"])

        if policy is None:
            errors.append(
                f"{endorsement_id}: referenced policy does not exist."
            )
            continue

        product = product_by_id.get(policy["product_id"])

        if product is None:
            errors.append(
                f"{endorsement_id}: product does not exist."
            )
            continue

        previous = endorsement["previous_coverage"]
        new = endorsement["new_coverage"]
        limit = product["max_coverage"]

        if previous <= 0 or new <= 0:
            errors.append(
                f"{endorsement_id}: coverage must be positive."
            )

        if new > limit:
            errors.append(
                f"{endorsement_id}: new coverage exceeds product limit."
            )

        if previous > limit:
            errors.append(
                f"{endorsement_id}: previous coverage exceeds product limit."
            )

        if endorsement.get("status") == "APPLIED":
            if policy.get("status") != "ACTIVE":
                errors.append(
                    f"{endorsement_id}: applied endorsement "
                    "belongs to a non-active policy."
                )

           
            if float(policy["coverage"]) != float(new):
             errors.append(
             f"{endorsement_id}: current coverage does not "
              "match the applied endorsement."
    )


    return errors


def validate_renewals(renewals, policies):
    """Cancelled policies must not receive renewal offers."""

    errors = []

    policy_by_id = {
        policy["policy_id"]: policy
        for policy in policies
    }

    for renewal in renewals:
        policy = policy_by_id.get(renewal["policy_id"])

        if policy is None:
            errors.append(
                f"{renewal['renewal_id']}: referenced policy "
                "does not exist."
            )
            continue

        if policy["status"] == "CANCELLED":
            errors.append(
                f"{renewal['renewal_id']}: renewal exists "
                "for a cancelled policy."
            )

        if renewal["offered_premium"] <= 0:
            errors.append(
                f"{renewal['renewal_id']}: premium must be positive."
            )

    return errors


# def validate_overlapping_policies(policies):
#     """
#     Detect overlapping periods for the same asset and product.
#     Add permitted exceptions explicitly in a future rule configuration.
#     """

#     errors = []

#     grouped = {}

#     for policy in policies:
#         key = (policy["asset_id"], policy["product_id"])
#         grouped.setdefault(key, []).append(policy)

#     for (asset_id, product_id), records in grouped.items():
#         records = sorted(
#             records,
#             key=lambda p: p["start_date"]
#         )

#         for index in range(len(records)):
#             first = records[index]

#             if first["status"] == "CANCELLED":
#                 first_end = first.get("cancellation_date")
#             else:
#                 first_end = first["end_date"]

#             if not first_end:
#                 continue

#             for second in records[index + 1:]:
#                 if second["status"] == "CANCELLED":
#                     second_end = second.get("cancellation_date")
#                 else:
#                     second_end = second["end_date"]

#                 if not second_end:
#                     continue

#                 if (
#                     first["start_date"] <= second_end
#                     and second["start_date"] <= first_end
#                 ):
#                     errors.append(
#                         f"Overlapping policies: {first['policy_id']} "
#                         f"and {second['policy_id']} for asset "
#                         f"{asset_id}, product {product_id}."
#                     )




def validate_overlapping_policies(policies):
    errors = []

    active_policies = [
        policy for policy in policies
        if policy.get("status") == "ACTIVE"
    ]

    for i, policy_a in enumerate(active_policies):
        for policy_b in active_policies[i + 1:]:
            # Compare policies for the same asset and product.
            if (
                policy_a.get("asset_id") != policy_b.get("asset_id")
                or policy_a.get("product_id") != policy_b.get("product_id")
            ):
                continue

            start_a = policy_a["start_date"]
            end_a = policy_a["end_date"]
            start_b = policy_b["start_date"]
            end_b = policy_b["end_date"]

            # Date strings in YYYY-MM-DD format can be compared directly.
            if start_a < end_b and start_b < end_a:
                errors.append(
                    f"Overlapping policy periods: "
                    f"{policy_a['policy_id']} and {policy_b['policy_id']}"
                )

    return errors

                    
     
def validate_policy_acceptance(policies):
    """Flag policies issued without customer acceptance."""
    errors = []

    for policy in policies:
        if str(policy.get("accepted", "")).strip().lower() != "true":
            errors.append({
                "policy_id": policy.get("policy_id"),
                "error": "POLICY_WITHOUT_ACCEPTANCE",
            })

    return errors

     
                    

    return errors
