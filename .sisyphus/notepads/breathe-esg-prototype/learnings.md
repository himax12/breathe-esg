# Breathe ESG Prototype - Learnings

## Architecture Decisions

### Data Model: Append-Only + Corrections Table (NOT Event Sourcing)
- ESG data is **periodic batch files**, not real-time streams
- Event sourcing (CQRS, event store) is over-engineered for this data type
- Append-only records with corrections as new rows gives audit immutability at lower complexity
- Evaluator might push back: "why not event sourcing?" → Answer: batch file cadence doesn't need stream processing patterns

### Scope 2: Location-Only (NOT Dual Reporting)
- Market-based Scope 2 requires modeling contractual instruments (PPAs, RECs, supplier-specific rates)
- Without that model, showing "scope_2_market" would be a misleading zero or null
- Honest approach: location-only + `contractual_instruments_present` enum
- Evaluator might push back: "GHG Protocol requires dual reporting" → Answer: only when contractual instruments are present, and we document the gap

### Approval State: Simple (NOT Amendment State Machine)
- ESG restatements = new submission records, not mutations of existing records
- APPROVED → AMENDED transition conflates submission state with record state
- Correct model: `reporting_submission` table tracking period + submission date + status + superseded_by
- For MVP: simple APPROVED / FLAGGED / REJECTED state, document amendment as production feature

### Flag Detection: Threshold Rules (NOT Statistical)
- Statistical anomaly detection requires historical baseline data
- We don't have that baseline in prototype
- Threshold rules (value > X, field missing) are explainable to non-technical analysts
- Evaluator might push back: "this is simplistic" → Answer: documented as production feature with ML-based approach

### Ingestion: File Upload (NOT API Pull)
- Real API connectors (SAP OData, Concur OAuth, utility portals) require weeks of integration work
- File upload with realistic sample data demonstrates the pipeline concept
- Evaluator might push back: "this is not realistic" → Answer: documented gap with production API path

### Multi-Tenancy: Single-Tenant (NOT Row-Level Security)
- Real multi-tenancy requires django-tenants or PostgreSQL RLS
- `client_id` column is NOT multi-tenancy — it's single-tenant with a label
- Evaluator might push back: "requirement says multi-tenancy" → Answer: documented production architecture options

## Source Format Research

### SAP IDoc Structure
- Control record: EDI_DC40 (IDoc number, direction, sender/receiver)
- Data records: segments (E1EDK01 header, E1EDP01 line items)
- Actual data in SDATA string field (1000 chars)
- For fuel: FIDCCP02 or custom Z-IDoc with MATNR, MENGE, MEINS, WERKS, BWART
- NOT building real IDoc parser — CSV with SAP field names is sufficient for prototype

### Utility Portal Export
- Facilities teams typically export CSV from portal
- Portal CSV has: meter_id, billing_period_start/end, consumption_kwh, demand_kva, tariff_code
- PDF bills are a separate problem (weeks of PDF parsing work)
- Billing periods often don't align with calendar months (e.g., 23rd to 22nd)

### Concur/Travel API
- REST API with OAuth 2.0
- Endpoints: /expenses, /trips, /travelers
- Returns: origin/destination (IATA codes), distance (sometimes), amount
- Direct API requires app registration, approval flow
- CSV with Concur-style structure is sufficient for prototype

## Normalization Factors (IPCC AR6)

```
Diesel combustion: 2.68 kg CO2 per liter
Gasoline combustion: 2.31 kg CO2 per liter
Grid electricity (eGRID 2024): varies by region, ~0.4-0.5 kg CO2 per kWh average
Flight short-haul (<1500km): 0.147 kg CO2 per km
Flight long-haul (≥1500km): 0.195 kg CO2 per km
Hotel per night: 27.1 kg CO2 per night (average)
Diesel car: 0.171 kg CO2 per km
Petrol car: 0.156 kg CO2 per km
```

## What Could Go Wrong

1. **Underestimating time**: Django + React + Deploy + Docs in 2 days is tight
   - Mitigation: have a "cut this first" list (flag modal, sorting, pagination)

2. **Render deployment issues**: PostgreSQL on free tier can be slow
   - Mitigation: test locally first, have backup plan (Railway)

3. **Sample data not looking realistic**: evaluator asks "why does this data look this way?"
   - Mitigation: SOURCES.md research is critical — must show we researched real formats

4. **Evaluators asking about event sourcing**: if they know CQRS and push back
   - Mitigation: "batch file cadence" argument is solid — but must be able to explain why we chose simpler

5. **Scope 2 dual reporting pushback**: GHG Protocol technically requires it
   - Mitigation: "we don't have contractual instrument data" is honest but might sound like ignorance
   - Better: show the enum field `contractual_instruments_present` that would drive dual reporting in production