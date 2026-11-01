# Synthetic Insurance Data Generator

A Python-based data engineering project that generates realistic synthetic insurance datasets and injects controlled anomalies for data quality validation and testing.

## Project Overview

This project simulates an insurance workflow, including applicants, insured assets, insurance products, quotes, underwriting decisions, policies, endorsements, and renewals.

It generates reproducible synthetic data using a fixed random seed and validates business rules to identify expected anomalies and unexpected data quality errors.

## Features

- Generates synthetic insurance workflow datasets.
- Supports reproducible generation using seed `2026`.
- Injects five types of labeled anomalies.
- Validates relationships and business rules across datasets.
- Exports datasets as CSV files.
- Produces a JSON validation report.
- Includes automated tests using pytest.

## Dataset Summary

| Dataset | Records |
|---|---:|
| Applicants | 3,000 |
| Assets | 3,000 |
| Quotes | 4,000 |
| Underwriting decisions | 4,000 |
| Policies | 2,002 |
| Renewals | 1,201 |
| Endorsements | 1 |

Ground-truth labels: **84**.

## Injected Anomalies

| Anomaly type | Count |
|---|---:|
| `PREMIUM_ANOMALY` | 80 |
| `POLICY_WITHOUT_ACCEPTANCE` | 1 |
| `ENDORSEMENT_EXCEEDS_PRODUCT_LIMIT` | 1 |
| `RENEWAL_FOR_CANCELLED_POLICY` | 1 |
| `OVERLAPPING_POLICY_PERIODS` | 1 |

## Technology Stack

- Python
- CSV and JSON
- pytest
- Synthetic data generation
- Business-rule validation

## Project Structure

```text
insurance-data-generator/
├── generator/
│   └── edge_case_generator.py
├── validation/
│   ├── business_rules.py
│   ├── endorsements.py
│   └── foreign_keys.py
├── output/
│   ├── applicants.csv
│   ├── assets.csv
│   ├── quotes.csv
│   ├── underwriting_decisions.csv
│   ├── policies.csv
│   ├── renewals.csv
│   ├── endorsements.csv
│   ├── ground_truth.csv
│   └── validation_report.json
├── generate_data.py
├── validate_data.py
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd insurance-data-generator
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the datasets

```bash
python generate_data.py
```

### 5. Run automated tests

```bash
python -m pytest -q
```

### 6. Validate the generated data

```bash
python validate_data.py
```

## Validation Results

The current generated dataset passes validation with:

- 9 automated tests passed.
- 80 expected premium anomalies detected.
- 4 expected non-premium anomaly findings.
- 0 unexpected validation errors.

The validation report is saved to `output/validation_report.json`.

## Reproducibility

The generator uses seed `2026` to make synthetic data generation reproducible, provided the generation logic and dependencies remain unchanged.

## Disclaimer

All generated records are synthetic and intended for software development, testing, and demonstration. They do not represent real policyholders or actual insurance contracts.

## Future Improvements

- Add a data profiling dashboard.
- Generate visual summaries of anomalies.
- Add configurable dataset sizes and anomaly rates.
- Integrate automated data quality reporting.
- Add a database export option.
