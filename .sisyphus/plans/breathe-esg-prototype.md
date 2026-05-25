# Breathe ESG - ESG Data Ingestion & Review Prototype

## Problem Statement

Breathe ESG ingests emissions and activity data from client companies (SAP fuel/procurement, utility electricity, corporate travel), normalizes it, and surfaces a review dashboard where analysts approve rows before audit lock.

**Target:** Django REST + React prototype, deployed live, with full documentation.

**Grading:** Data model (35%), decision defense (25%), realistic source handling (20%), analyst UX (10%), what was NOT built (10%)

**Timeline:** 2 days compressed MVP

---

## Deliverables

| Deliverable | Description |
|---|---|
| **Working app (deployed)** | Django REST backend + React frontend on Render |
| **MODEL.md** | Data model decisions with rationale |
| **DECISIONS.md** | Every ambiguity resolved with why |
| **TRADEOFFS.md** | 3 deliberate non-builds with production paths |
| **SOURCES.md** | Research on each source format, sample data justification |

---

## Data Model

### Core Principle: Append-Only Records + Corrections Table

ESG data comes from **periodic batch files**, not real-time streams. Event sourcing is over-engineered. The correct pattern:
- **EmissionRecord**: immutable once created (no UPDATE, only INSERT)
- **Corrections table**: corrections are new rows, original stays in audit trail

### Models

```
EmissionRecord (main fact table)
├── id: UUID (PK)
├── batch_id: FK(ImportBatch)
├── source_type: Enum (SAP_FUEL, SAP_PROCUREMENT, UTILITY_ELECTRICITY, CORPORATE_TRAVEL)
├── source_location_code: String
├── source_location_type: Enum (SAP_PLANT, UTILITY_METER, AIRPORT)
├── raw_data: JSON (entire source row)
├── raw_value: Decimal
├── raw_unit: String
├── normalized_value: Decimal (SI: kg CO2e, kWh, km)
├── normalized_unit: String
├── conversion_factor: Decimal
├── conversion_factor_source: String
├── scope: Enum (SCOPE_1, SCOPE_2_LOCATION, SCOPE_3)
├── activity_type: String
├── period_start: Date
├── period_end: Date
├── status: Enum (PENDING, APPROVED, FLAGGED, REJECTED)
├── flag_type: String (nullable)
├── flag_reason: Text (nullable)
├── created_at: DateTime

ImportBatch
├── id: UUID (PK)
├── source_type: Enum
├── file_name: String
├── rows_total: Integer
├── rows_succeeded: Integer
├── rows_failed: Integer
├── status: Enum (UPLOADING, VALIDATING, IMPORTED, REVIEW_IN_PROGRESS, COMPLETED)
├── total_kgCO2_scope1: Decimal
├── total_kgCO2_scope2_location: Decimal
├── total_kgCO2_scope3: Decimal

DataFlag (threshold rules config)
├── id: UUID (PK)
├── source_type: Enum
├── field_name: String
├── rule_type: Enum (MIN_VALUE, MAX_VALUE, REQUIRED)
├── threshold_value: Decimal
├── active: Boolean

ApprovalLog
├── id: UUID (PK)
├── record_id: FK(EmissionRecord)
├── action: Enum (APPROVED, FLAGGED, REJECTED, NOTE_ADDED)
├── performed_by: String
├── performed_at: DateTime
├── note: Text (nullable)
```

### Why NOT Event Sourcing
- ESG is batch file imports, not real-time streams
- Append-only + corrections table gives audit immutability without CQRS complexity
- The evaluator asks "why" — this is explainable in 2 minutes

### Why NOT Dual Scope 2 Reporting
- Market-based Scope 2 requires contractual instrument modeling (PPAs, RECs)
- Without that model, showing "scope_2_market" would be a misleading zero
- Location-only with `contractual_instruments_present` enum is honest

---

## Normalization Rules

```
SAP Fuel: liters → kg CO2e
  - Diesel: 2.68 kg CO2/L (IPCC AR6 GWP100)
  - Gasoline: 2.31 kg CO2/L

SAP Procurement: "each" → cannot normalize without material-specific factors
  - Stored as raw, flagged for manual review

Utility Electricity: kWh → kg CO2e
  - Grid factor: eGRID 2024 (region-specific) or UK DARC
  - Stored: consumption_kwh, grid_region, factor_version

Corporate Travel (flight): distance_km → kg CO2e
  - Short haul (<1500km): 0.147 kg CO2/km
  - Long haul (≥1500km): 0.195 kg CO2/km

Corporate Travel (hotel): night → kg CO2e
  - Average: 27.1 kg CO2/night

Corporate Travel (ground): distance_km → kg CO2e
  - Diesel car: 0.171 kg CO2/km
  - Petrol car: 0.156 kg CO2/km
```

---

## Ingestion Architecture

### File Upload (per source type)

```
POST /api/upload/sap-fuel
POST /api/upload/sap-procurement
POST /api/upload/utility-electricity
POST /api/upload/corporate-travel
```

**Flow:**
1. Validate CSV structure (required columns present)
2. Parse row-by-row
3. Apply threshold flag rules
4. Normalize units → SI
5. Assign scope (source-type-based default)
6. Bulk create EmissionRecord rows
7. Return import summary

### Flag Rules (Threshold-Based)

```
SAP Fuel:
  - MENGE (quantity) > 50,000 L/day → FLAG
  - MEINS (unit) missing → FLAG

Utility Electricity:
  - consumption_kwh > 50,000 kWh/month → FLAG
  - meter_id missing → FLAG

Corporate Travel:
  - distance_km missing for FLIGHT → FLAG (only origin/dest given)
  - amount_local > 100,000 → FLAG (possible data error)
```

### Why NOT Statistical Anomaly Detection
- Statistical methods require historical data baseline
- In a prototype, we don't have that baseline
- Threshold rules are explainable to non-technical analysts
- Documented as production feature

---

## API Endpoints

```
# Ingestion
POST   /api/upload/{source_type}         — upload CSV, returns batch summary

# Batches
GET    /api/batches/                     — list all batches with aggregates
GET    /api/batches/{id}/               — batch detail

# Records
GET    /api/batches/{id}/records/        — paginated rows (filter: status, flag_type)
POST   /api/batches/{id}/approve-batch/  — approve all PENDING rows

# Row Actions
POST   /api/records/{id}/approve/        — approve single row
POST   /api/records/{id}/flag/           — flag row with note
POST   /api/records/{id}/reject/         — reject row

# Audit
GET    /api/records/{id}/history/        — approval log for record
```

---

## Frontend Pages

### 1. Import List (`/`)
- Table: batch ID, source, date, row counts, status, total emissions by scope
- Click → batch detail

### 2. Batch Detail (`/batches/{id}`)
- Summary cards: total rows, flagged count, approval progress bar
- Filter tabs: All | Pending | Flagged | Approved | Rejected
- Data table: source location | raw value | unit | kg CO2e | scope | status
- Batch action: "Approve All Pending" with confirmation modal

### 3. Flag Modal
- Shows flagged record details
- Text field: reason
- Dropdown: flag category (MISSING_FIELD, VALUE_OUT_OF_RANGE, OTHER)

---

## Sample Data

### SAP Fuel (FIDCCP02-style CSV)
```
Filename: sap_fuel_export_2024_Q1.csv
Headers (German): WERKS, BWART, MATNR, MENGE, MEINS, BUDAT
- 50 rows, mix of diesel/gasoline
- Realistic plant codes: DE01, DE02, NL01
- German date format: DD.MM.YYYY
- One outlier: 50,000L single day entry
- Missing MEINS on 3 rows
```

### Utility Electricity (portal CSV)
```
Filename: utility_electricity_2024_Q1.csv
Headers: meter_id, billing_period_start, billing_period_end, consumption_kwh, demand_kva, tariff_code
- 30 rows, monthly billing periods
- One missing meter_id
- One consumption > 10x average (meter malfunction flagged)
```

### Corporate Travel (Concur-style CSV)
```
Filename: concur_travel_2024_Q1.csv
Headers: employee_id, trip_date, category, origin, destination, distance_km, amount_local, currency
- 40 rows, mix of FLIGHT/HOTEL/GROUND
- Missing distance_km on some flights (only airport codes given)
- Realistic IATA codes: LHR, JFK, DEL, BOM
```

---

## What We Are NOT Building (TRADEOFFS.md)

### 1. Real SAP API Connector
**Not built:** Direct SAP OData/BAPI integration
**Why:** Requires SAP Gateway, RFC connection, ABAP authority — weeks of work
**Production path:** SAP REST API adapter using OAuth + SAP OData services

### 2. Scope 2 Market-Based Reporting
**Not built:** Dual Scope 2 (location + market)
**Why:** Requires modeling contractual instruments (PPAs, RECs, supplier-specific rates) — domain problem
**Production path:** ContractualInstrument model + market-based factor lookup

### 3. Real Multi-Tenancy
**Not built:** Schema isolation or row-level security
**Why:** Requires django-tenants or PostgreSQL RLS — architectural decision beyond prototype
**Production path:** django-tenants with per-client PostgreSQL schema OR PostgreSQL RLS

---

## Deployment (Render)

- Django REST API + PostgreSQL (Render free tier)
- React frontend (build → static files served by Django)
- `render.yaml` for Render blueprint
- `python manage.py migrate` on deploy
- Sample data pre-loaded via management command

---

## Documentation Deliverables

| File | Content |
|---|---|
| MODEL.md | Why append-only + corrections, why single Scope 2, why threshold rules, why single-tenant |
| DECISIONS.md | SAP format choice, utility format choice, travel format choice, scope categorization, amendment path |
| TRADEOFFS.md | Real SAP connector, Scope 2 dual reporting, multi-tenancy — each with production path |
| SOURCES.md | IDoc structure findings, portal export research, Concur API research, sample data justification |

---

## Execution Plan (2 Days)

### Day 1 — Backend
| Time | Task |
|---|---|
| Morning | Django project + models + migrations |
| Midday | CSV upload + parsing + normalization |
| Afternoon | Flag rules + API endpoints |
| Evening | Verify with curl (upload, query, approve) |

### Day 2 — Frontend + Deploy + Docs
| Time | Task |
|---|---|
| Morning | React dashboard (list + detail + table) |
| Midday | Sample data fabrication |
| Afternoon | Deploy to Render + verify live |
| Evening | Write 4 documentation files |

---

## Success Criteria

- [ ] All 4 documentation files written and defensible
- [ ] App deployed and accessible at live URL
- [ ] Can upload CSV, see records in dashboard, approve/reject rows
- [ ] Evaluator can navigate and understand the decisions
- [ ] Each "not built" has documented production path