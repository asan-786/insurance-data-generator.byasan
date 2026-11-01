
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = PROJECT_ROOT / "config" / "products.json"


def load_products():
    """Load product definitions from the JSON configuration file."""
    if not PRODUCTS_FILE.exists():
        raise FileNotFoundError(
            f"Products configuration not found: {PRODUCTS_FILE}"
        )

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        config = json.load(file)

    products = config.get("products", [])
    if not products:
        raise ValueError("No products found in products.json")

    required_fields = {
        "product_id",
        "product_name",
        "product_line",
        "max_coverage",
        "base_premium",
    }

    product_ids = set()
    product_lines = set()

    for product in products:
        missing = required_fields - product.keys()
        if missing:
            raise ValueError(
                f"Product is missing required fields: {sorted(missing)}"
            )

        if product["product_id"] in product_ids:
            raise ValueError(
                f"Duplicate product ID: {product['product_id']}"
            )

        if product["product_line"] in product_lines:
            raise ValueError(
                f"Duplicate product line: {product['product_line']}"
            )

        if product["max_coverage"] <= 0:
            raise ValueError("Maximum coverage must be positive")

        if product["base_premium"] < 0:
            raise ValueError("Base premium cannot be negative")

        product_ids.add(product["product_id"])
        product_lines.add(product["product_line"])

    if len(products) != 3:
        raise ValueError(
            f"Expected 3 products, but found {len(products)}"
        )

    return products


if __name__ == "__main__":
    products = load_products()

    print(f"Successfully loaded {len(products)} products:\n")

    for product in products:
        print(
            f"{product['product_id']} | "
            f"{product['product_name']} | "
            f"Max coverage: INR {product['max_coverage']:,} | "
            f"Base premium: INR {product['base_premium']:,}"
        )
