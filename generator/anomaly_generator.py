
import random


def inject_anomalies(
    quotes,
    seed=2026,
    anomaly_rate=0.02
):
    """
    Inject controlled premium anomalies into quote records.

    Returns:
        modified_quotes: quote records with selected anomalies
        ground_truth: labels describing the injected anomalies
    """
    if not 0 <= anomaly_rate <= 1:
        raise ValueError("anomaly_rate must be between 0 and 1.")

    rng = random.Random(seed)

    # Work on copies so the caller's original records aren't mutated.
    modified_quotes = [quote.copy() for quote in quotes]
    ground_truth = []

    anomaly_count = int(len(modified_quotes) * anomaly_rate)

    if anomaly_count == 0:
        return modified_quotes, ground_truth

    selected_indices = rng.sample(
        range(len(modified_quotes)),
        anomaly_count
    )

    for index in selected_indices:
        quote = modified_quotes[index]

        original_premium = float(quote["premium"])

        # Apply a reproducible, deliberately abnormal premium increase.
        multiplier = rng.choice([2.0, 3.0, 5.0])
        quote["premium"] = round(
            original_premium * multiplier,
            2
        )

        ground_truth.append({
            "entity_type": "quote",
            "entity_id": quote["quote_id"],
            "issue_type": "PREMIUM_ANOMALY",
            "field_name": "premium",
            "original_value": original_premium,
            "anomalous_value": quote["premium"],
            "multiplier": multiplier,
            "is_anomaly": True,
        })

    return modified_quotes, ground_truth
