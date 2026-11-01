
# import csv
# from pathlib import Path

# OUTPUT_DIR = Path("output")


# def read_csv(filename):
#     with open(
#         OUTPUT_DIR / filename,
#         newline="",
#         encoding="utf-8"
#     ) as file:
#         return list(csv.DictReader(file))


# def main():
#     quotes = read_csv("quotes.csv")
#     decisions = read_csv("underwriting_decisions.csv")
#     policies = read_csv("policies.csv")

#     quote_by_id = {
#         row["quote_id"]: row for row in quotes
#     }

#     decision_by_quote = {
#         row["quote_id"]: row for row in decisions
#     }

#     anomalies = read_csv("ground_truth.csv")
#     anomaly_ids = {
#         row["entity_id"] for row in anomalies
#         if row["issue_type"] == "PREMIUM_ANOMALY"
#     }

#     missing_decisions = []
#     missing_policy_quotes = []
#     anomalous_policies = []

#     for quote in quotes:
#         quote_id = quote["quote_id"]

#         if quote_id not in decision_by_quote:
#             missing_decisions.append(quote_id)

#     for policy in policies:
#         quote_id = policy["quote_id"]

#         if quote_id not in quote_by_id:
#             missing_policy_quotes.append(quote_id)
#             continue

#         if quote_id in anomaly_ids:
#             anomalous_policies.append({
#                 "policy_id": policy["policy_id"],
#                 "quote_id": quote_id,
#                 "quote_premium": quote_by_id[quote_id]["premium"],
#                 "policy_premium": policy["premium"],
#             })

#     print("Quotes:", len(quotes))
#     print("Underwriting decisions:", len(decisions))
#     print("Policies:", len(policies))
#     print("Missing underwriting decisions:", len(missing_decisions))
#     print("Policies referencing missing quotes:", len(missing_policy_quotes))
#     print("Policies linked to anomalous quotes:", len(anomalous_policies))

#     if anomalous_policies:
#         print("\nFirst 10 policies linked to anomalous quotes:")
#         for row in anomalous_policies[:10]:
#             print(row)


# if __name__ == "__main__":
#     main()











import csv
from pathlib import Path

OUTPUT_DIR = Path("output")


def read_csv(filename):
    with open(
        OUTPUT_DIR / filename,
        newline="",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def main():
    quotes = read_csv("quotes.csv")
    policies = read_csv("policies.csv")
    ground_truth = read_csv("ground_truth.csv")

    quote_by_id = {
        row["quote_id"]: row for row in quotes
    }

    labels_by_id = {
        row["entity_id"]: row
        for row in ground_truth
        if row["issue_type"] == "PREMIUM_ANOMALY"
    }

    quote_policy_mismatches = []
    original_value_mismatches = []
    labeled_quote_count = 0

    for quote_id, label in labels_by_id.items():
        quote = quote_by_id.get(quote_id)

        if quote is None:
            original_value_mismatches.append(
                f"Missing quote: {quote_id}"
            )
            continue

        labeled_quote_count += 1

        actual = float(quote["premium"])
        expected = float(label["anomalous_value"])
        original = float(label["original_value"])

        if abs(actual - expected) > 0.01:
            original_value_mismatches.append(
                f"{quote_id}: expected anomalous premium "
                f"{expected}, found {actual}"
            )

        if abs(actual - original) < 0.01:
            original_value_mismatches.append(
                f"{quote_id}: labeled anomaly has unchanged "
                f"premium {actual}"
            )

    for policy in policies:
        quote_id = policy["quote_id"]
        quote = quote_by_id.get(quote_id)

        if quote is None:
            continue

        quote_premium = float(quote["premium"])
        policy_premium = float(policy["premium"])

        if abs(quote_premium - policy_premium) > 0.01:
            quote_policy_mismatches.append(
                f"{policy['policy_id']}: quote={quote_premium}, "
                f"policy={policy_premium}"
            )

    print("Labeled anomaly quotes checked:", labeled_quote_count)
    print("Incorrect anomaly labels:", len(original_value_mismatches))
    print("Quote-policy premium mismatches:", len(quote_policy_mismatches))

    if original_value_mismatches:
        print("\nAnomaly label issues:")
        for error in original_value_mismatches[:10]:
            print(error)

    if quote_policy_mismatches:
        print("\nQuote-policy mismatches:")
        for error in quote_policy_mismatches[:10]:
            print(error)

    if not original_value_mismatches and not quote_policy_mismatches:
        print("\nAll checks passed.")


if __name__ == "__main__":
    main()
