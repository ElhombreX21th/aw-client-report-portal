# Field Service Operations — KPI & Job Costing Sample Report

**Type:** Public portfolio demonstration · **Dataset:** 100% synthetic · **Currency:** USD · **Prepared:** 29 October 2026

> This is an illustrative business-operations analysis created for a job application. It does not use any customer data, employer data, actual job-management exports, Workiz API access, or measured business outcomes. The analysis demonstrates an approach, not a production deployment or a client engagement.

## Executive summary

This sample models ten completed field-service jobs with revenue and direct costs. It demonstrates how a business owner can obtain consistent unit economics and clear weekly KPIs after reconciling duplicate records.

| Illustrative KPI | Result | Meaning |
|---|---:|---|
| Completed jobs | 10 | Unique completed job IDs |
| Revenue | **$6,620.00** | Sum of sample job revenues |
| Direct cost | **$2,799.00** | Labor + materials + other direct costs |
| Gross profit | **$3,821.00** | Revenue minus direct cost |
| Weighted gross margin | **57.72%** | Gross profit / revenue (not mean of row margins) |
| Labor hours | **57.0 h** | Sum of hours |
| Revenue per labor hour | **$116.14/h** | Revenue / labor hours |
| Illustrative close rate | **62.5%** | 10 won jobs / 16 qualified quoted opportunities, separately assumed |

### Assumptions

- A fully loaded **direct labor cost of $32/hour** is used for every sample job. The rate is an exercise assumption, not an industry benchmark.
- Materials and other costs are direct job expenses; overhead, tax, and owner compensation are excluded. **Gross margin is not net profit.**
- The 16 quoted opportunities and 10 wins are illustrative funnel counts, **not** inferred from the completed-job table.
- All rows have IDs and completion status; duplicates are removed by job ID only after inspecting timestamps/source authority.

## Reconciled sample job data

| Job ID | Revenue ($) | Labor (h) | Materials ($) | Other direct ($) | Total direct ($) | Gross profit ($) |
|---|---:|---:|---:|---:|---:|---:|
| FS-001 | 420 | 4.0 | 35 | 20 | 183 | 237 |
| FS-002 | 650 | 6.0 | 65 | 25 | 282 | 368 |
| FS-003 | 360 | 3.0 | 30 | 15 | 141 | 219 |
| FS-004 | 880 | 8.0 | 100 | 40 | 396 | 484 |
| FS-005 | 510 | 4.5 | 45 | 30 | 219 | 291 |
| FS-006 | 750 | 7.0 | 70 | 45 | 339 | 411 |
| FS-007 | 300 | 2.5 | 25 | 15 | 120 | 180 |
| FS-008 | 1,150 | 9.0 | 120 | 65 | 473 | 677 |
| FS-009 | 620 | 5.0 | 50 | 25 | 235 | 385 |
| FS-010 | 980 | 8.0 | 105 | 50 | 411 | 569 |
| **TOTAL** | **6,620** | **57.0** | **645** | **330** | **2,799** | **3,821** |

**Calculation rules**
- `direct_labor_cost = labor_hours * 32`
- `direct_job_cost = direct_labor_cost + materials_cost + other_direct_cost`
- `gross_profit = job_revenue - direct_job_cost`
- `gross_margin_percent = 100 * SUM(gross_profit) / SUM(job_revenue)`
- `revenue_per_labor_hour = SUM(job_revenue) / SUM(labor_hours)`

## Reconciliation and automation design

1. **Ingest:** collect exports from job-management, labor-time, and invoicing systems. Preserve source ID, update time, timezone, currency, and import batch ID.
2. **Normalize:** standardize job IDs, completion timestamps, numeric fields, currencies, and status mapping. Keep raw data immutable.
3. **Reconcile:** distinguish legitimate multiple invoices for a job from accidental duplicate records. Resolve conflicts by a documented source-of-truth rule, not blind `DISTINCT`.
4. **Validate:** flag missing job IDs, negative or implausible costs, jobs with zero labor, unknown status, unmatched invoices, and large differences between source and KPI totals.
5. **Aggregate:** compute weighted gross margin, revenue/labor hour, close rate (with a separately reconciled quote funnel), and exception counts.
6. **Deliver:** publish owner-friendly weekly summaries and exceptions, with a traceable link back to source records. A future design could use Python, SQL, REST APIs/webhooks and Slack messages.

### Example read-only SQL logic (illustrative)

```sql
SELECT
    COUNT(*) AS completed_jobs,
    ROUND(SUM(revenue), 2) AS revenue_usd,
    ROUND(SUM(labor_hours * 32 + materials + other_direct), 2) AS direct_cost_usd,
    ROUND(SUM(revenue - (labor_hours * 32 + materials + other_direct)), 2) AS gross_profit_usd,
    ROUND(
      100 * SUM(revenue - (labor_hours * 32 + materials + other_direct))
      / NULLIF(SUM(revenue), 0), 2
    ) AS weighted_gross_margin_pct,
    ROUND(SUM(revenue) / NULLIF(SUM(labor_hours), 0), 2) AS revenue_per_labor_hour
FROM reconciled_jobs
WHERE status = 'completed';
```

**Proposed verification:** compare source-system financial totals against job-level aggregates, sample source records manually, and log reconciliation exceptions before automating an executive alert. No automated Workiz, Slack, or client integration is claimed by this sample.

## Related public implementation evidence

- [AW Client Report Portal](https://github.com/ElhombreX21th/aw-client-report-portal): FastAPI-based financial-reporting prototype with example UI, calculations and PDF output.
- [ReembolsaBR API](https://github.com/ElhombreX21th/Main-Repository): Python/FastAPI, data models, SQL-oriented workflows, authorization and audit-log architecture.
- [OPSPECTA RCA Copilot](https://github.com/FPConnect/fpconnect-rca-copilot): MedTech service-operations and diagnostic-assistance project.

These are projects/prototypes and are not presented as verified production services, paid contracts, or work performed for KC Power Clean.

**Portfolio author:** Flavio Pimenta da Cruz · [LinkedIn](https://www.linkedin.com/in/flavio-cruz-09751820/) · [GitHub](https://github.com/ElhombreX21th)
