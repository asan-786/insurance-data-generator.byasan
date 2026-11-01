# Insurance Synthetic Data Generator — Data Dictionary

## 1. Applicant
- `applicant_id`: String, primary key, format `APP-YYYY-NNNNNN`
- `full_name`: String, required
- `date_of_birth`: Date, required
- `email`: String, optional
- `created_at`: Timestamp, required

## 2. InsuredAsset
- `asset_id`: String, primary key
- `applicant_id`: String, foreign key to Applicant
- `asset_type`: Enum: MOTOR, PROPERTY, SMALL_BUSINESS
- `asset_value`: Decimal, greater than zero
- `created_at`: Timestamp

## 3. Product
- `product_id`: String, primary key
- `product_name`: String, required
- `product_line`: Enum: MOTOR, PROPERTY, SMALL_BUSINESS
- `max_coverage`: Decimal, greater than zero
- `base_premium`: Decimal, non-negative

## 4. CoverageOption
- `coverage_id`: String, primary key
- `coverage_name`: String, required
- `coverage_limit`: Decimal, greater than zero

## 5. RiskFactor
- `risk_factor_id`: String, primary key
- `factor_name`: String, required
- `factor_value`: String, required
- `factor_weight`: Decimal, required

## 6. Quote
- `quote_id`: String, primary key, format `QTE-YYYY-NNNNNN`
- `applicant_id`: Foreign key to Applicant
- `asset_id`: Foreign key to InsuredAsset
- `product_id`: Foreign key to Product
- `requested_coverage`: Decimal, greater than zero
- `premium`: Decimal, calculated from pricing rules
- `status`: Enum: DRAFT, SUBMITTED, REFERRED, ACCEPTED, DECLINED, EXPIRED
- `created_at`: Timestamp

## 7. UnderwritingDecision
- `decision_id`: String, primary key
- `quote_id`: Foreign key to Quote
- `decision`: Enum: APPROVED, REFERRED, DECLINED
- `reason_code`: String, required
- `decision_at`: Timestamp

## 8. Policy
- `policy_id`: String, primary key, format `POL-YYYY-NNNNNN`
- `quote_id`: Unique foreign key to Quote
- `accepted`: Boolean
- `payment_completed`: Boolean
- `start_date`: Date
- `end_date`: Date, must be after start_date
- `status`: Enum: ACTIVE, CANCELLED, EXPIRED

## 9. Endorsement
- `endorsement_id`: String, primary key
- `policy_id`: Foreign key to Policy
- `previous_coverage`: Decimal
- `new_coverage`: Decimal
- `effective_date`: Date
- `status`: Enum: PENDING, APPROVED, REJECTED, APPLIED

## 10. Renewal
- `renewal_id`: String, primary key
- `policy_id`: Foreign key to Policy
- `renewal_year`: Integer
- `offered_premium`: Decimal
- `status`: Enum: OFFERED, ACCEPTED, DECLINED, EXPIRED, RENEWED

## 11. EntityEvent
- `event_id`: String, primary key
- `entity_type`: String
- `entity_id`: String
- `event_type`: String
- `previous_state`: String, optional
- `new_state`: String, optional
- `reason`: String
- `event_timestamp`: Timestamp

## General Rules
- All IDs must be unique and generated consistently.
- Foreign keys must reference existing records.
- Premiums must follow the configured pricing formula.
- Policies may only be issued when mandatory acceptance and payment conditions are satisfied.
- Endorsements and renewals must preserve historical information.
- All monetary values use INR.
- Intentional invalid test cases must be labelled separately in ground truth.
