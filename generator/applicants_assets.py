
import random
from datetime import date, timedelta
from pathlib import Path
import sys

from faker import Faker

# Allow imports from the generator folder
sys.path.insert(0, str(Path(__file__).resolve().parent))

from id_generator import IDGenerator

fake = Faker()


def generate_applicants_assets(count=10, seed=2026):
    """Generate fictional applicants and insured assets."""
    random.seed(seed)
    Faker.seed(seed)
    fake.seed_instance(seed)

    ids = IDGenerator(year=2026)

    applicants = []
    assets = []

    product_lines = ["MOTOR", "PROPERTY", "SMALL_BUSINESS"]

    for _ in range(count):
        applicant_id = ids.generate("applicant")

        birth_date = fake.date_of_birth(
            minimum_age=21,
            maximum_age=70
        )

        applicants.append({
            "applicant_id": applicant_id,
            "full_name": fake.name(),
            "date_of_birth": birth_date.isoformat(),
            "email": fake.unique.email(),
            "created_at": "2026-01-01T10:00:00"
        })

        asset_id = ids.generate("asset")
        asset_type = random.choice(product_lines)

        assets.append({
            "asset_id": asset_id,
            "applicant_id": applicant_id,
            "asset_type": asset_type,
            "asset_value": round(
                random.uniform(100000, 5000000), 2
            ),
            "created_at": "2026-01-01T10:00:00"
        })

    return applicants, assets


if __name__ == "__main__":
    applicants, assets = generate_applicants_assets(
        count=10,
        seed=2026
    )

    print(f"Generated {len(applicants)} applicants")
    print(f"Generated {len(assets)} assets")
    print("\nFirst applicant:")
    print(applicants[0])
    print("\nFirst asset:")
    print(assets[0])
