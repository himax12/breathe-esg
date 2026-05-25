# MODEL.md — Breathe ESG Data Model Documentation

## Overview

This document describes the data model for the Breathe ESG prototype — an emissions data ingestion and review system. It explains the design decisions, the rationale behind each choice, and what production systems would require.

**Core principle:** ESG data arrives as periodic batch files, not real-time streams. This shapes every architectural decision.

---

## Architecture: Append-Only Records + Corrections Table

### Why Not Event Sourcing?

Event sourcing (CQRS, event stores) is the correct pattern for real-time data streams — financial trading systems, IoT sensor networks, logistics tracking. ESG data is not that.

ESG data arrives as:
- SAP exports (daily/weekly/monthly batch)
- Utility portal CSV downloads (monthly billing cycles)
- Travel expense reports (weekly)

The "event" is the file import, not an underlying activity. The activity (fuel consumption, electricity use) is already in the past when we receive it.

**Therefore:** We use append-only records with a corrections table, not event sourcing.

```
EmissionRecord: immutable once created (no UPDATE, only INSERT)
CorrectionRecord: new row that supersedes original, original stays in audit trail
```

### Audit Immutability

Once an EmissionRecord is created, it is never modified. The `status` field can change (PENDING → APPROVED → FLAGGED), but this is a state transition logged in ApprovalLog, not a data mutation.

**Why this matters for ESG:** Auditors need to prove that what was reported matched what was locked at the time of audit. If records could be mutated, the audit trail is worthless.

---

## Data Model

### ImportBatch

Represents one CSV file upload.

```
ImportBatch
├── id: UUID (PK)
├── source_type: SAP_FUEL | SAP_PROCUREMENT | UTILITY_ELECTRICITY | CORPORATE_TRAVEL
├── file_name: String
├── rows_total: Integer
├── rows_succeeded: Integer
├── rows_failed: Integer
├── status: UPLOADING | VALIDATING | IMPORTED | REVIEW_IN_PROGRESS | COMPLETED
├── total_kgCO2_scope1: Decimal (computed on approval)
├── total_kgCO2_scope2_location: Decimal
├── total_kgCO2_scope3: Decimal
├── imported_at: DateTime
├── imported_by: String (nullable)
```

**Design decisions:**
- `source_type` is a string enum, not a foreign key. ESG source systems don't have an API we model — they produce files. The enum is sufficient.
- Aggregates are cached on the batch for dashboard performance. They're recomputed when records are approved.

---

### EmissionRecord

One row per emission event from a source file.

```
EmissionRecord
├── id: UUID (PK)
├── batch: FK(ImportBatch)
├── source_type: String
├── source_location_code: String (plant_code | meter_id | airport_code)
├── source_location_type: SAP_PLANT | UTILITY_METER | AIRPORT
├── raw_data: JSON (entire source row as received)
├── raw_value: Decimal
├── raw_unit: String
├── normalized_value: Decimal (SI: kg CO2e, kWh, km)
├── normalized_unit: String
├── conversion_factor: Decimal
├── conversion_factor_source: String (e.g., "IPCC AR6 GWP100")
├── scope: SCOPE_1 | SCOPE_2_LOCATION | SCOPE_3
├── activity_type: String
├── period_start: Date
├── period_end: Date
├── status: PENDING | APPROVED | FLAGGED | REJECTED
├── flag_type: MISSING_FIELD | VALUE_OUT_OF_RANGE | OTHER
├── flag_reason: Text
├── flag_score: Integer (0-3, number of signals triggered)
├── created_at: DateTime
├── created_by: String (nullable)
```

**Design decisions:**

1. **raw_data JSON field:** Stores the entire source row as received. This preserves the original format for audit replay. If we need to re-parse the file (e.g., correction factor changes), we have the original data.

2. **Separate raw and normalized values:** raw_value/raw_unit preserved for audit. normalized_value/normalied_unit computed at ingest time. This solves the "what if the conversion factor is wrong" problem — we can re-normalize from raw_data.

3. **Scope categorization:** Source-based default (SAP fuel → SCOPE_1, utility electricity → SCOPE_2_LOCATION, corporate travel → SCOPE_3). Manual override is available but not modeled as a separate field — the analyst changes the scope enum directly.

4. **Why NOT Scope 2 dual reporting (location + market):** GHG Protocol requires dual reporting only when contractual instruments (PPAs, RECs, supplier-specific rates) are present. Without modeling contractual instruments, showing a "market-based value" would be a misleading zero. We document this gap in DECISIONS.md.

5. **flag_score (0-3):** Threshold-based scoring, not statistical anomaly detection. Requires no historical baseline. Each rule triggered adds 1 to the score.

---

### DataFlag

Threshold rules configuration for flagging records at import time.

```
DataFlag
├── id: UUID (PK)
├── source_type: String
├── field_name: String (JSON path within raw_data)
├── rule_type: MIN_VALUE | MAX_VALUE | REQUIRED
├── threshold_value: Decimal (nullable for REQUIRED)
├── active: Boolean
```

**Design decisions:**
- Stored in database, not code. Allows rule updates without deployment.
- Field name is a string path (e.g., "MENGE" for SAP, "consumption_kwh" for utility). The path is evaluated against raw_data JSON at import time.
- REQUIRED rules check if field is absent or blank.
- MAX_VALUE rules check if numeric value exceeds threshold.

**Default rules:**
- SAP Fuel: MENGE > 50,000 L/day → flagged. MEINS missing → flagged.
- Utility: meter_id missing → flagged. consumption_kwh > 50,000 kWh/month → flagged.
- Corporate Travel: distance_km missing for FLIGHT → flagged.

---

### ApprovalLog

Immutable audit trail of every action taken on a record.

```
ApprovalLog
├── id: UUID (PK)
├── record: FK(EmissionRecord)
├── action: APPROVED | FLAGGED | REJECTED | NOTE_ADDED
├── performed_by: String (default: 'analyst')
├── performed_at: DateTime
├── note: Text
```

**Design decisions:**
- Every state transition is logged. The ApprovalLog is append-only — no updates, no deletes.
- `performed_by` is a string for MVP (no auth). Production would use a foreign key to User.
- `note` captures context: why a record was flagged, why approved despite flags, etc.

---

## Normalization Rules

### Fuel Combustion (SAP Fuel → Scope 1)

```
Diesel: 2.68 kg CO2 per liter (IPCC AR6 GWP100)
Gasoline: 2.31 kg CO2 per liter (IPCC AR6 GWP100)
```

Determined from material number (MATNR). Default to diesel if ambiguous.

### Grid Electricity (Utility → Scope 2 Location-Based)

```
Average grid factor: 0.42 kg CO2 per kWh (eGRID 2024 average)
```

Regional factors available but not modeled in MVP. Production would store region-specific grid factors.

### Business Travel (Corporate Travel → Scope 3)

```
Flight short-haul (<1500km): 0.147 kg CO2 per km (DEFRA 2024)
Flight long-haul (≥1500km): 0.195 kg CO2 per km (DEFRA 2024)
Hotel per night: 27.1 kg CO2 per night (EPA 2022)
Ground transport (diesel car): 0.171 kg CO2 per km (DEFRA 2024)
```

---

## What Production Would Require

### Real Multi-Tenancy

Current: Single-tenant with hardcoded client context.

Production options:
1. **django-tenants** with PostgreSQL schema per client
2. **Row-level security** with PostgreSQL RLS policies

Current prototype is NOT multi-tenant — it's a single-client demo with a client_id field not implemented.

### Contractual Instruments for Scope 2 Market-Based

Scope 2 market-based requires modeling: PPAs, RECs, supplier-specific emission rates. This is a domain data modeling problem, not a software problem. Production would require:
- ContractualInstrument model (issuer, type, issuance date, expiration, quantity)
- Market-based factor lookup based on contractual instrument held

### Amendment/Restatement Support

Current: APPROVED is immutable.

Production ESG systems (ESOS, SEC, CSRD) require restatement capability — when methodology changes or errors are found, prior periods can be restated. Production would require:
- ReportingPeriod model (period, submission_date, status)
- SUPERSEDED transition that creates new record instead of mutating original

### Historical Baseline for Anomaly Detection

Current flag rules are threshold-based (no historical data required). Statistical anomaly detection (values > 3 std dev from mean) requires a baseline that we don't have in prototype. Production would require:
- Historical data accumulation
- Per-client, per-source-type baseline computation
- Machine learning or statistical threshold calculation

---

## Database Constraints

```python
class EmissionRecord(models.Model):
    # No UPDATE allowed on approved records — enforced at application level
    # Future: database-level constraint with trigger
    
    # Append-only: raw_data is never mutated after creation
    # Status changes are logged in ApprovalLog, not mutations
```

---

## Schema Evolution

New source types (IoT sensors, Salesforce, custom ERP) → new columns added to raw_data JSON, no migration required.

Production would require:
- Schema version table tracking when each field was added/deprecated
- Quarterly schema cleanup process (archive deprecated columns)
- View layer hiding deprecated fields from analyst dashboard