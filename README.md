# Insurance Data Generator

A Python-based synthetic insurance data generation and validation project that creates realistic, interconnected insurance datasets and checks them against business rules.

This project demonstrates data generation, business-rule validation, automated testing, and data quality assurance. It is designed to make the generated data reproducible, inspectable, and easier to verify.

## Overview

Insurance systems manage interconnected information about applicants, assets, quotes, underwriting decisions, policies, renewals, and endorsements. Maintaining consistency across these records is important for reliable downstream analysis and testing.

The Insurance Data Generator creates synthetic insurance records and validates their consistency using business rules. It also supports testing with intentionally anomalous records to help identify potential data quality and business logic issues.

> **Note:** The project generates synthetic data. It is not an insurance pricing engine, an underwriting recommendation system, or a production insurance platform.

## Key Features

- **Synthetic data generation:** Generate insurance-related records for testing and experimentation.
- **Multiple related datasets:** Create records covering applicants, assets, quotes, underwriting decisions, policies, renewals, endorsements, and ground-truth labels.
- **Business-rule validation:** Check generated data for inconsistencies and invalid relationships.
- **Anomaly detection:** Identify selected insurance data anomalies, including:
  - Premium anomalies.
  - Policies without acceptance.
  - Endorsements exceeding product limits.
  - Renewals associated with cancelled policies.
  - Overlapping policy periods.
- **Automated testing:** Run the project's test suite with `pytest`.
- **Validation reporting:** Execute the validation pipeline and review its overall result and unexpected errors.

## Technology Stack

- **Language:** Python
- **Testing:** pytest
- **Data processing:** Python-based generation and validation logic
- **Version control:** Git and GitHub

The exact dependencies are defined by the project's dependency files, if provided.

## Project Structure

```text
insurance-data-generator/
├── generator/
│   └── # Data generation modules
├── validation/
│   └── # Business rules and validation logic
├── tests/
│   └── # Automated tests
├── output/
│   └── # Generated datasets
├── generate_data.py
├── validate_data.py
├── .gitignore
└── README.md
```

The directory structure above summarizes the main project components. Individual files may vary according to the current repository version.

## Getting Started

### 1. Prerequisites

Install Python and Git. Python 3.10 or newer is a reasonable starting point, but use the version supported by the project's actual dependencies.

Check your installation:

```bash
python --version
git --version
```

### 2. Clone the repository

```bash
git clone https://github.com/asan-786/insurance-data-generator.byasan.git
cd insurance-data-generator
```

### 3. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

If the repository includes a `requirements.txt` file, run:

```bash
python -m pip install -r requirements.txt
```

If no dependency file is present, install the project's actual required packages as documented in the source code. The test suite requires `pytest`.

## Running the Project

Run the following commands from the project root.

### Generate synthetic data

```bash
python generate_data.py
```

This executes the data generation pipeline and writes its outputs to the configured output location.

### Validate generated data

```bash
python validate_data.py
```

This executes the validation pipeline and reports the overall validation result and any unexpected errors.

### Run automated tests

```bash
python -m pytest -q
```

This runs the project's automated test suite in quiet mode.

## Generated Datasets

The project generates the following categories of insurance data:

| Dataset | Purpose |
|---|---|
| Applicants | Synthetic applicant records |
| Assets | Information about insured assets |
| Quotes | Insurance quote records |
| Underwriting decisions | Underwriting decision records |
| Policies | Policy records |
| Renewals | Policy renewal records |
| Endorsements | Policy amendment records |
| Ground-truth labels | Labels associated with selected records or anomalies |

The exact schemas, relationships, row counts, and output formats should be verified against the generated files and current implementation.

## Validation and Testing

The project uses business rules to identify data inconsistencies and potential anomalies.

Examples of checks include:

- Whether policies have the required acceptance status.
- Whether endorsement values remain within product limits.
- Whether renewals are consistent with policy cancellation status.
- Whether policy periods overlap unexpectedly.
- Whether premium values exhibit defined anomalies.

Validation results depend on the implemented rules and the generated dataset. A successful validation run does not establish that every possible insurance business rule is covered.

### Previously verified results

During development, the project was verified with the following results:

| Check | Result |
|---|---|
| Data generation | Successful |
| Validation pipeline | PASS |
| Unexpected validation errors | 0 |
| Automated tests | 9 passed |

These are previously observed development results, not a guarantee for every future run or repository version. Re-run the commands above to verify the current version.

## Design Decisions

### Why synthetic data?

Synthetic data allows development and testing without relying on real customer or policyholder information. It also makes it possible to construct scenarios for testing business rules and data quality checks.

### Why separate generation and validation?

Separating data generation from validation keeps the responsibilities easier to understand and test. Generated records can be inspected independently, while validation logic can be improved without mixing it into the generation process.

### Why automated tests?

Automated tests help detect regressions when generation logic, data relationships, or business rules change. They provide a repeatable way to verify expected behavior during development.

## Assumptions and Limitations

- The data is synthetic and should not be interpreted as actual customer or insurance company data.
- The implemented business rules represent only the scenarios covered by the current code.
- Generated records and row counts may vary between runs depending on the implementation and configuration.
- The project does not establish compliance with any specific insurance regulation or production underwriting standard.
- Any known incomplete features or limitations should be documented here as development continues.

## Reproducibility

To reproduce the basic development checks, run:

```bash
python generate_data.py
python validate_data.py
python -m pytest -q
```

Review the console output and generated datasets to confirm the results. Record the Python version, dependency versions, and any configuration required to reproduce a particular run.

## AI Usage and Development Transparency

This project follows the YottaFlex AI candidate-project requirement for transparent AI usage.

AI tools may be used for assistance, but the submitted work must remain the candidate's individual work. The candidate should be able to explain the core logic, dependencies, design decisions, testing approach, and limitations.

Document the actual AI usage in a file such as:

`docs/AI_PROMPT_HISTORY.md`

Include:

- The prompts submitted to each AI tool used.
- The areas where AI assistance accelerated development.
- The code and design decisions personally reviewed or modified.
- The tests and validations personally performed.
- Any limitations in recording prompt history.

Do not invent historical prompts or claim independent verification that was not performed. AI responses may be included, but the candidate project FAQ states that they are optional.

## Security and Data Privacy

- Do not commit API keys, passwords, access tokens, or other credentials.
- Do not include real customer records or sensitive personal information.
- Keep virtual environments, local secrets, caches, and unnecessary generated artifacts out of Git.
- Use synthetic or otherwise authorized sample data.

## Future Improvements

Potential future enhancements, depending on project requirements, include:

- Configurable dataset sizes and generation parameters.
- More comprehensive cross-dataset integrity checks.
- Additional anomaly scenarios and validation tests.
- Reproducible random seeds and documented configurations.
- Structured validation reports with counts and explanations.
- Schema documentation and example output samples.

These are possible improvements, not claims that the features are already implemented.

## Author

**Asan Ali**

GitHub: [asan-786](https://github.com/asan-786)

## License

A license has not been specified in this README. Add an appropriate license file if you intend to publish the project under a particular open-source license.

---

*Developed as a synthetic insurance data generation and validation project. The repository's source code, tests, and documented execution results are the authoritative references for implemented functionality.*





USED AI ->


# AI Prompt History and Usage Disclosure

**Project:** Insurance Data Generator
**Candidate:** Asan Ali
**Repository:** [https://github.com/asan-786/insurance-data-generator.byasan](https://github.com/asan-786/insurance-data-generator.byasan)
**AI tool documented:** ChatGPT (OpenAI)
**Date prepared:** 1 November 2026

## 1. Purpose

This document records the use of AI assistance during development, testing, troubleshooting, and documentation of the Insurance Data Generator.

ChatGPT was used as an assistant to help understand technical issues, explore debugging approaches, prepare documentation, and organize the project for submission. The candidate remains responsible for reviewing the code, understanding the implementation, and verifying the final results.

This document distinguishes prompts visible in the available conversation from summaries of earlier activities whose complete original wording is unavailable.

## 2. AI Tool Disclosure

| Tool             | Usage                                                                           | Record status                                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| ChatGPT (OpenAI) | Troubleshooting, validation guidance, Git assistance, and project documentation | [https://chatgpt.com/share/6ae6ebdf-cc04-83ee-afb4-13bb2a3b64f0](https://chatgpt.com/share/6ae6ebdf-cc04-83ee-afb4-13bb2a3b64f0) |
| Other AI tools   | cloud                                                                           | partialy used                                                                                                                    |

The table should be updated to reflect every AI tool actually used for this project.

## 3. Available Prompt History

The following prompts are reproduced from the available conversation. They relate to preparing the project for recruitment submission and documenting its development.

### Prompt 1 — Create the project README

**AI tool:** ChatGPT
**Project area:** `README.md`
**Prompt status:** Verbatim from the available conversation

> Create a professional GitHub README for my existing insurance-data-generator project, based on the YottaFlex AI submission requirements and known project details.

**Purpose:** Obtain a professional README structure covering project functionality, setup, execution, validation, testing, limitations, and AI usage disclosure.

**Review and verification:** The README must be checked against the actual source code and repository structure. Commands, dependencies, features, and test results must be verified before submission.

### Prompt 2 — Prepare the AI prompt-history document

**AI tool:** ChatGPT
**Project area:** `docs/AI_PROMPT_HISTORY.md`
**Prompt status:** Verbatim from the available conversation

> Help me prepare an honest AI prompt-history document for my YottaFlex AI candidate project. Do not invent prompts I have not supplied; explain how to record and disclose them.

**Purpose:** Prepare an honest disclosure that distinguishes available original prompts from reconstructed summaries and explains how to record AI assistance.

**Review and verification:** The document must be compared with available conversation histories and records from all AI tools used.

### Prompt 3 — Add ChatGPT and prepare the final output

**AI tool:** ChatGPT
**Project area:** AI usage disclosure
**Prompt status:** Verbatim from the available conversation

**Purpose:** Include ChatGPT in the AI usage disclosure and produce a consolidated document.

**Review and verification:** The document identifies ChatGPT as an AI tool and separates available prompts from activity summaries whose original wording is unavailable.

## 4. Earlier Project-Related AI Assistance

The available project context also records earlier assistance. The following are summaries, **not verbatim historical prompts**.

### 4.1 Business-rule validation

**Relevant file:** `validation/business_rules.py`

Assistance involved troubleshooting a policy validation issue concerning the coverage field. The relevant implementation detail recorded in the project context was that the policy uses `coverage`, rather than `current_coverage`.

The recorded development results subsequently showed that the validation pipeline passed with zero unexpected errors.

**Verification required:** Inspect the final implementation and rerun validation against the committed code.

### 4.2 Data generation and automated testing

**Relevant files:** `generate_data.py`, `validate_data.py`, and `tests/`

Assistance involved project execution, debugging, and validation troubleshooting.

Previously recorded results indicated successful data generation, a passing validation pipeline, and nine passing automated tests.

The following commands were used to verify the project:

```bash
python generate_data.py
python validate_data.py
python -m pytest -q
```

These are commands recorded in the project context. Their results must be reproduced against the final submitted version before they are described as freshly verified.

### 4.3 Git and GitHub publication

Assistance was provided for publishing the project to GitHub, including guidance for resolving a merge conflict in `README.md` and completing the repository push.

**Verification required:** Confirm that the conflict was resolved, the merge was committed, and the latest project files are present in the public repository.

### 4.4 Documentation and recruitment preparation

Assistance was provided to interpret the YottaFlex AI candidate-project requirements, prepare the README, and structure the AI usage disclosure.

The candidate should review all generated documentation, correct any inaccuracies, and ensure the final repository accurately represents the implemented functionality.

## 5. How AI Assisted

Based on the available project history, ChatGPT assisted with:

- Understanding and troubleshooting a business-rule validation issue.
- Reviewing project execution and validation steps.
- Explaining Git merge-conflict resolution and GitHub publication commands.
- Structuring the README and project documentation.
- Preparing a transparent AI usage disclosure for recruitment submission.

These activities describe the assistance documented in the available context. They are not an exhaustive record of every interaction during development.

## 6. Candidate Contributions and Verification

The following statements must be completed or confirmed by the candidate before submission.

### Code review

I reviewed the project files and checked the AI suggestions against the actual implementation.

### Implementation changes

I evaluated proposed changes and retained or modified the implementation as appropriate.

### Testing

I executed the relevant commands and examined the results before submitting the project.

### Technical understanding

I am prepared to explain the data generation workflow, the implemented business rules, the validation process, the automated tests, and the limitations of the project.

Only retain statements that accurately describe your own work and understanding.

## 7. Limitations of This Record

This document was prepared from the project context and conversation records available during its preparation. It does not establish that every historical prompt from every AI tool has been recovered.

Some earlier development interactions are represented by summaries because their complete original wording is not available in the current record.

To complete the prompt history:

1. Review the relevant ChatGPT conversations and copy additional original prompts.
2. Check any other AI coding assistants used during development and include their prompts.
3. Label any reconstructed summaries clearly.
4. If a tool cannot export its prompts, preserve the records that can be recovered and disclose the limitation.
5. Do not invent prompts, dates, test results, or personal contributions.

AI responses are not included in full because the YottaFlex AI FAQ states that responses are optional.

## 8. Security and Privacy

Before publishing this document:

- Remove passwords, API keys, tokens, and other credentials.
- Do not include personal or sensitive information.
- Ensure that only authorized code and safe synthetic data are included in the public repository.

## 9. Final Submission Checklist

- [ ] All AI tools actually used are disclosed.
- [ ] Available original prompts are included.
- [ ] Historical prompts that could not be recovered are disclosed honestly.
- [ ] Reconstructed summaries are labeled as summaries.
- [ ] Personal contributions and AI assistance are distinguished.
- [ ] Test results are accurate and verified against the final version.
- [ ] The README matches the implementation.
- [ ] No secrets or unauthorized code are included.
- [ ] The final document is committed to the public GitHub repository.

## 10. Candidate Declaration

I have prepared this document to disclose AI assistance used during the development and preparation of the Insurance Data Generator. I will review the final document against the available records, add any missing prompts that I can recover, and disclose limitations honestly. I am responsible for understanding the submitted implementation and ensuring that statements about my contributions and verification are accurate.

**Candidate:** Asan Ali
**Date prepared:** 1 November 2026

