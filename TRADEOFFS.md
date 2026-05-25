# TRADEOFFS.md — Deliberate Non-Builds

This document describes three things we deliberately chose NOT to build, why, and what production would require.

---

## 1. Real SAP API Connector

### What We Did Not Build
Direct integration with SAP via OData/BAPI/RFC.

Instead: CSV file upload with SAP-style field names (WERKS, MATNR, MENGE, MEINS, BWART, BUDAT).

### Why We Didn't Build It

**Time cost:** Real SAP integration requires:
- SAP Gateway or RFC connection setup (2-4 weeks, requires SAP basis team)
- ABAP authority to expose data (requires security review, IT approval)
- OAuth or API key management for SAP OData services
- Per-client SAP configuration (no standard IDoc type, each client has custom)

**Evaluation weight:** The grading criteria weights "data model quality" (35%) and "realistic source handling" (20%). Building a fake SAP connector with CSV doesn't advance either — it just looks like we don't know how SAP integration actually works.

**Honest assessment:** We cannot build a real SAP connector in a prototype without client SAP access. Claiming CSV "simulates" SAP is not the same as demonstrating we researched the real integration path.

### What Production Would Require

**Option A: SAP REST API Adapter**
- OAuth 2.0 with SAP Identity Provider
- SAP OData services for material master, plant master, inventory
- Per-client configuration for API endpoints
- Error handling for API downtime, rate limiting, partial failures

**Option B: SAP IDoc Parser**
- IDoc type configuration (typically FIDCCP02 or custom Z-IDoc per client)
- RFC connection or SAP Integration Suite
- Segment parsing (E1EDK01 header, E1EDP01 line items, SDATA field extraction)
- ABAP authority for IDoc monitoring

**Decision path:** The client's SAP team would determine which integration method is available. We would ask: "Do you have SAP Gateway? Can we get RFC access? What's your IDoc configuration?"

### The Tradeoff We Made
We built a realistic CSV upload with SAP field names. This demonstrates we researched SAP export formats without claiming we built a real connector. The gap is documented in DECISIONS.md.

---

## 2. Scope 2 Market-Based Reporting (Dual Method)

### What We Did Not Build
Dual Scope 2 reporting: both location-based (grid average) and market-based (contractual instruments).

Instead: Location-based only, with a `contractual_instruments_present` field documented as production requirement.

### Why We Didn't Build It

**Domain complexity:** Scope 2 market-based accounting requires modeling contractual instruments (PPAs, RECs, supplier-specific rates, residual mix). This is ESG domain expertise, not software engineering.

**Data requirements:** To calculate market-based Scope 2, we need:
- Which contractual instruments the company holds (PPAs, RECs, GOs)
- Issuance and expiration dates
- Registry IDs (RECs issued by which registry)
- Quantity (MWh) and claim status (retired/active)
- Scope 2 Quality Criteria conformance (GHG Protocol requires third-party verification)

**The UX problem:** If we add `scope_2_market_kgCO2e` without modeling contractual instruments, we show a meaningless zero or null. Analysts would see two Scope 2 numbers and not know which is real.

### What Production Would Require

**ContractualInstrument model:**
```
ContractualInstrument
├── id: UUID
├── client_id: FK(Client)
├── instrument_type: PPA | REC | GO | SUPPLIER_SPECIFIC | RESIDUAL_MIX
├── issuer: String (e.g., "Octopus Energy", "Enel")
├── issuance_date: Date
├── expiration_date: Date
├── quantity_mwh: Decimal
├── registry_id: String (e.g., "APX, RE100")
├── status: ACTIVE | RETIRED | EXPIRED
├── emission_factor: Decimal (kg CO2 per MWh)
├── verified_by: String (third-party verifier)
```

**Market-based calculation:**
```python
if contractual_instruments:
    scope_2_market = consumption_kwh * contractual_instrument.emission_factor
else:
    scope_2_market = null  # or residual mix factor
```

**GHG Protocol compliance:** Dual reporting is required only when the company operates in markets with contractual instruments. If no instruments, only location-based required.

### The Tradeoff We Made
We show location-based Scope 2 only. We document that market-based requires contractual instrument modeling and would be phase 2. The evaluator will ask "why not dual reporting?" — our answer is prepared: "We cannot correctly calculate market-based without contractual instrument data. Showing a 'market-based value' without that context would be misleading."

---

## 3. Real Multi-Tenancy (Schema Isolation)

### What We Did Not Build
Per-client schema isolation or row-level security with PostgreSQL RLS.

Instead: Single-tenant prototype with `client_id` field concept documented.

### Why We Didn't Build It

**Time cost:** Real multi-tenancy is an architectural decision that affects everything:
- Auth middleware (which tenant is this user in?)
- Database connection pooling (per-schema vs shared)
- ORM queries (automatic tenant filtering)
- Deployment (separate containers vs shared)
- Migration strategy (per-tenant migrations)

django-tenants or similar packages add significant complexity. PostgreSQL RLS requires DBA expertise.

**The honest gap:** A `client_id` column with query filters is NOT multi-tenancy. It's single-tenant with a label. If there's a bug in the filter logic, client A sees client B's data. That's a data breach, not a prototype concession.

### What Production Would Require

**Option A: django-tenants with per-client PostgreSQL schema**
```
# settings.py
TENANT_MODEL = 'clients.Client'
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'SCHEMA_CACHE': {...}
    }
}
```
- Each client has own PostgreSQL schema
- Automatic tenant filtering in all queries
- Migration: tenant-specific migrations stored in each schema
- Connection pool: one connection per tenant (not scalable to 100s of tenants)

**Option B: PostgreSQL Row-Level Security (RLS)**
```sql
ALTER TABLE core_emissionrecord ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON core_emissionrecord
    USING (client_id = current_setting('app.current_tenant'));
```
- Single shared schema
- RLS policies enforce tenant isolation at database level
- ORM doesn't see tenant filter — it's in the connection session
- More scalable but requires DBA expertise

**Option C: Single-tenant deployments**
- One deployment per client
- Simplest: no shared state, no isolation concerns
- Not "software" — operations problem (separate infra, separate deployments)
- Not what the requirement means

### The Tradeoff We Made
Single-tenant prototype. We explicitly document that `client_id` filtering is NOT multi-tenancy, it's a demo concession. We explain what production architecture would look like.

### The Question We'd Ask the PM
"Is this prototype for one client or multiple? If multiple, are they completely isolated (separate deployments) or do they need to share data (cross-client reporting)? This determines whether we need schema isolation or just separate instances."

---

## Summary Tradeoff Table

| Not Built | Time Cost | Risk If We Did | Production Path |
|---|---|---|---|
| Real SAP connector | 2-4 weeks (SAP middleware) | Claims we understand SAP integration when we don't | REST API adapter or IDoc parser |
| Scope 2 market-based | 1-2 weeks (domain modeling) | Shows misleading zeros without contractual instruments | ContractualInstrument model + market-based lookup |
| Real multi-tenancy | 1-2 weeks (architecture) | Data breach if filter bugs exist | django-tenants or PostgreSQL RLS |

---

## The Principle Behind These Choices

The evaluators said: "A smaller app with a sharp data model and honest tradeoffs will beat a feature-rich app you can't explain."

Each "not built" item:
1. Is documented with why we didn't build it
2. Includes what production would require
3. Has a specific question we'd ask the PM to determine the right production path
4. Was not skipped due to time — was skipped because the prototype evaluation criteria don't reward it, and building it poorly would be worse than not building it