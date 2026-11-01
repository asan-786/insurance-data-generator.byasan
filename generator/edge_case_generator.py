
def inject_policy_without_acceptance(policies):
    """Create an intentionally invalid policy and its ground-truth label."""

    if not policies:
        raise ValueError("At least one policy is required.")

    original_policy = policies[0].copy()
    anomalous_policy = original_policy.copy()

    anomalous_policy["policy_id"] = (
        f"{original_policy['policy_id']}-EDGE-001"
    )
    anomalous_policy["accepted"] = False

    label = {
        "entity_type": "policy",
        "entity_id": anomalous_policy["policy_id"],
        "issue_type": "POLICY_WITHOUT_ACCEPTANCE",
        "field_name": "accepted",
        "original_value": True,
        "anomalous_value": False,
        "multiplier": "",
        "is_anomaly": True,
    }

    return anomalous_policy, label

    
    



def inject_endorsement_limit_violation(policy, product):
    """Create an endorsement exceeding the product coverage limit."""

    max_coverage = float(product["max_coverage"])
    original_coverage = float(policy["coverage"])

    if original_coverage > max_coverage:
        raise ValueError(
            "Selected policy already exceeds the product coverage limit."
        )

    anomalous_coverage = round(max_coverage + 1000, 2)

    endorsement = {
        "endorsement_id": f"END-{policy['policy_id']}-EDGE-001",
        "policy_id": policy["policy_id"],
        "previous_coverage": original_coverage,
        "new_coverage": anomalous_coverage,
        "effective_date": policy["start_date"],
        "status": "APPLIED",
    }

    # Keep the policy and applied endorsement consistent.
    policy["coverage"] = anomalous_coverage

    label = {
        "entity_type": "endorsement",
        "entity_id": endorsement["endorsement_id"],
        "issue_type": "ENDORSEMENT_EXCEEDS_PRODUCT_LIMIT",
        "field_name": "new_coverage",
        "original_value": max_coverage,
        "anomalous_value": anomalous_coverage,
        "multiplier": "",
        "is_anomaly": True,
    }

    return endorsement, label


    
    

def inject_renewal_for_cancelled_policy(policy, renewal_year):
    """Create a cancelled policy and a renewal linked to it."""

    cancelled_policy = policy.copy()
    cancelled_policy["status"] = "CANCELLED"

    renewal = {
        "renewal_id": (
            f"REN-{cancelled_policy['policy_id']}-"
            f"{renewal_year}-EDGE-001"
        ),
        "policy_id": cancelled_policy["policy_id"],
        "renewal_year": renewal_year,
        "offered_premium": round(
            float(cancelled_policy["premium"]) * 1.05, 2
        ),
        "status": "OFFERED",
    }

    label = {
        "entity_type": "renewal",
        "entity_id": renewal["renewal_id"],
        "issue_type": "RENEWAL_FOR_CANCELLED_POLICY",
        "field_name": "policy_status",
        "original_value": "ACTIVE",
        "anomalous_value": "CANCELLED",
        "multiplier": "",
        "is_anomaly": True,
    }

    return cancelled_policy, renewal, label


  
def inject_overlapping_policy(policies):
    """Create an intentionally overlapping policy and its ground-truth label."""

    if not policies:
        raise ValueError("At least one policy is required.")

    original_policy = next(
        (
            policy for policy in policies
            if policy.get("status") == "ACTIVE"
            and not policy.get("policy_id", "").endswith("-EDGE-001")
            and not policy.get("policy_id", "").endswith("-OVERLAP-EDGE-001")
        ),
        None,
    )

    if original_policy is None:
        raise ValueError("No suitable active policy found.")

    anomalous_policy = original_policy.copy()
    anomalous_policy["policy_id"] = (
        f"{original_policy['policy_id']}-OVERLAP-EDGE-001"
    )

    # Create a period that overlaps the original policy's period.
    anomalous_policy["start_date"] = original_policy["start_date"]
    anomalous_policy["end_date"] = original_policy["end_date"]
    anomalous_policy["status"] = "ACTIVE"

    label = {
        "entity_type": "policy",
        "entity_id": anomalous_policy["policy_id"],
        "issue_type": "OVERLAPPING_POLICY_PERIODS",
        "field_name": "policy_id",
        "original_value": original_policy["policy_id"],
        "anomalous_value": anomalous_policy["policy_id"],
        "multiplier": "",
        "is_anomaly": True,
    }

    return anomalous_policy, label

