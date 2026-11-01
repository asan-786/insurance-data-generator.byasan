
from collections import defaultdict


class IDGenerator:
    def __init__(self, year=2026):
        self.year = year
        self.counters = defaultdict(int)

    def generate(self, entity):
        self.counters[entity] += 1
        number = self.counters[entity]

        prefixes = {
            "applicant": "APP",
            "quote": "QTE",
            "policy": "POL",
            "asset": "AST",
            "product": "PRD",
            "coverage": "COV",
            "risk_factor": "RSK",
            "decision": "DEC",
        }

        if entity not in prefixes:
            raise ValueError(f"Unknown entity type: {entity}")

        prefix = prefixes[entity]
        return f"{prefix}-{self.year}-{number:06d}"

    def generate_endorsement(self, policy_id, sequence):
        return f"END-{policy_id}-{sequence:03d}"

    def generate_renewal(self, policy_id, renewal_year):
        return f"REN-{policy_id}-{renewal_year}"


if __name__ == "__main__":
    ids = IDGenerator(year=2026)

    print(ids.generate("applicant"))
    print(ids.generate("applicant"))
    print(ids.generate("quote"))
    print(ids.generate("policy"))

    policy_id = "POL-2026-000001"
    print(ids.generate_endorsement(policy_id, 1))
    print(ids.generate_renewal(policy_id, 2027))
