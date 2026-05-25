# DECISIONS.md — Design Decision Documentation

This document captures every ambiguity resolved during the prototype development, what we chose, why, and what we'd ask the PM if we could.

---

## 1. SAP Data Format: IDoc vs CSV

### The Ambiguity
SAP can export data via IDoc (Intermediate Document), flat file, OData service, BAPI, or RFC. Which format should we model?

### Research Findings
- IDocs are hierarchical with control records (EDI_DC40), segment structures (E1EDK01 for header, E1EDP01 for line items), and data in SDATA string fields (1000 chars per segment)
- IDocs require SAP middleware (SAP Gateway or RFC connection) and ABAP authority to configure
- Most companies with SAP export IDocs as flat files or use LSMW (Legacy System Migration Workbench) to convert to CSV
- SAP admins typically provide CSV exports that mirror IDoc field structure

### Decision
CSV file upload with SAP-style field names (WERKS, MATNR, MENGE, MEINS, BWART, BUDAT).

### Rationale
A real SAP IDoc parser requires:
1. SAP middleware access (weeks of setup)
2. RFC connection credentials (security review required)
3. ABAP authority (IT approval required)
4. IDoc type configuration per client (varies by SAP configuration)

This is integration work, not modeling work. The prototype cannot realistically build a real SAP connector. CSV with realistic SAP field names demonstrates we researched the format without claiming we built a real integration.

### What I'd Ask the PM
"If the client is willing to provide SAP access, which export method do they use: IDoc, LSMW CSV, or custom ABAP report? This determines whether we build a parser or a file receiver."

---

## 2. Utility Data Format: Portal CSV vs API vs PDF

### The Ambiguity
Utility data comes from portal CSV exports, PDF bills, or utility API. Which do we handle?

### Research Findings
- Most utility portals (US: Enel, ConEd, PG&E; UK: Octopus, EDF; EU: Eni, Vattenfall) offer CSV export of billing data
- PDF bills require OCR or structured extraction (weeks of work, many edge cases)
- Some utilities offer API access but requires registration, approval, and per-utility integration
- Facilities teams typically download CSV from portal and email to sustainability team

### Decision
CSV file upload with realistic portal export format (meter_id, billing_period_start/end, consumption_kwh, demand_kva, tariff_code).

### Rationale
CSV is the realistic workflow. Facilities teams export CSV. PDF parsing is a separate engineering problem (document processing). API integration is utility-specific and requires per-utility adapter development.

### What I'd Ask the PM
"Which utilities does this client use, and do they have portal access that allows CSV export? What's the current manual process for getting utility data to the sustainability team?"

---

## 3. Travel Data: Concur API vs CSV

### The Ambiguity
Travel data comes from Concur, Navan, or expense management systems. Do we integrate via API or CSV?

### Research Findings
- Concur has REST APIs (expenses, trips, travelers) with OAuth 2.0 authentication
- Concur API requires: app registration, approval flow, OAuth token management, rate limiting
- Most companies still use CSV export from Concur for sustainability reporting
- Navan (acquired by SAP) has similar API structure

### Decision
CSV file upload with Concur-style field names (employee_id, trip_date, category, origin, destination, distance_km, amount_local).

### Rationale
OAuth integration requires app registration and approval — not available in prototype timeframe. CSV is realistic: sustainability teams pull expense reports from Concur as CSV and upload to carbon accounting systems.

### What I'd Ask the PM
"Do you have existing Concur or Navan integration, and if so, which API version? This determines whether we build OAuth flow or file-based ingestion."

---

## 4. Scope Categorization: Source-Based Default vs Rule Engine

### The Ambiguity
How do we determine Scope 1/2/3 from source data?

### Research Findings
- GHG Protocol: Scope 1 = direct combustion (fuel), Scope 2 = purchased electricity, Scope 3 = indirect including business travel
- Scope 2 has two methods: location-based (grid average) and market-based (contractual instruments). Dual reporting required only when contractual instruments present.
- Scope determination is mostly deterministic from source type

### Decision
Source-based default with manual override. SAP fuel → Scope 1, utility electricity → Scope 2 location-based, corporate travel → Scope 3.

### Rationale
Rule engine (source + activity + location → scope) is correct but requires ESG domain expertise to build correctly. Manual override is available but in prototype, source type is sufficient for 95% of cases.

### What I'd Ask the PM
"Does this client have contractual instruments (PPAs, RECs, supplier-specific rates) that would require market-based Scope 2 reporting? If yes, we need to model contractual instruments as first-class entities."

---

## 5. Amendment/Restatement: How Do We Handle Corrections?

### The Ambiguity
When a client finds an error in Q1 data after Q2 review, what happens?

### Research Findings
- ESG regulations (ESOS, SEC, CSRD) require restatement capability when methodology changes or material errors found
- Financial audit: "amended" means new submission to regulator, original preserved in audit trail
- ESG restatements are new submissions, not mutations

### Decision
Not built in prototype. APPROVED is immutable. Document as production requirement.

### Rationale
Building correct amendment workflow requires understanding regulatory timelines (when can you restate? what triggers a restatement?). This is a domain problem beyond prototype scope.

### What I'd Ask the PM
"What is the restatement policy? Can analysts undo an approval, or is a new submission required? What triggers a restatement: methodology change, data error, or regulatory request?"

---

## 6. Flag Detection: Threshold vs Statistical Anomaly

### The Ambiguity
How do we detect suspicious data?

### Research Findings
- Statistical anomaly detection (values > 3 std dev from mean) requires historical baseline
- Production ESG systems use: threshold rules + delta comparison + missing data flags
- Multi-signal scoring reduces false positives vs single-signal

### Decision
Threshold rules only (stored in DataFlag table). No statistical anomaly detection.

### Rationale
Statistical methods require historical data baseline we don't have. Threshold rules are explainable to non-technical analysts. DataFlag table allows rule updates without deployment.

### What I'd Ask the PM
"What baseline data do you have? Do you have 12+ months of historical consumption for each facility? This determines whether we can implement statistical anomaly detection or must rely on threshold rules."

---

## 7. Normalization: Store Raw + SI vs Raw Only

### The Ambiguity
Do we store both raw source values and SI-converted values, or just raw?

### Decision
Store both raw and SI-normalized.

### Rationale
- Raw preserved: if conversion factor is wrong, we can re-compute from original
- SI stored: analyst dashboard doesn't need unit handling logic, analysts shouldn't need to know SAP uses liters while utility uses kWh
- Storage overhead is acceptable for ESG data volumes (tens of thousands of records per year, not billions)

### What I'd Ask the PM
"What emission factor database do you use? (IPCC, DEFRA, eGRID, custom?) Do factors get updated, and if so, how often? This determines whether we need re-computation capability."

---

## 8. Multi-Tenancy: client_id vs Schema Isolation

### The Ambiguity
The requirement says "must handle multi-tenancy." How do we implement?

### Decision
Not implemented. Single-tenant prototype with documented production paths.

### Rationale
Real multi-tenancy requires architectural decisions (schema-per-tenant vs row-level security) that affect everything from auth to database configuration. Building a `client_id` column and calling it "multi-tenancy" is dishonest — it provides no real data isolation.

### What I'd Ask the PM
"Is this prototype for one client or multiple? If multiple, do they need to see each other's data or are they completely isolated? This determines whether we need schema isolation or just separate deployments."

---

## 9. Ingestion: File Upload vs API Pull

### The Ambiguity
Should we poll source system APIs or receive file uploads?

### Decision
File upload for all sources.

### Rationale
Real API connectors require:
- SAP middleware / RFC credentials (weeks of access setup)
- Concur OAuth app registration and approval (weeks)
- Utility portal API integration (per-utility, no standard)

File upload is realistic: this is how clients actually send data in pilot phases. API integration is phase 2.

### What I'd Ask the PM
"What's the current data delivery process? Manual email with attachments? SFTP drop? Existing API? This tells us whether we're replacing a broken process or building net new."

---

## 10. Data Model: Two-Layer vs Single Table

### The Ambiguity
Some ESG systems use two-layer (raw ingestion + normalized consumption). Should we?

### Research Findings
- Production ESG systems (Persefoni, Watershed) use append-only event logs, not two-layer
- Two-layer was a proposal from initial design, but research shows production systems use append-only with corrections as new records
- ESG audit requires proving what was reported, not what the source said

### Decision
Single append-only table (EmissionRecord). Corrections are new rows, not updates.

### Rationale
Append-only + corrections table is simpler than two-layer and gives audit immutability. Two-layer adds CQRS complexity (write path vs read path sync) without benefit for batch file imports.

### What I'd Ask the PM
"How often do emission factors change? (IPCC updates ~5 years, grid factors ~1 year) When a factor changes, do you need to re-run historical data, or just use new factors going forward?"