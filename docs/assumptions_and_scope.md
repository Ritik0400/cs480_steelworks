## Assumptions

**Assumption 1**  
We assume all Excel files contain a common key (e.g., `Lot_ID`) that allows for relational mapping, even if the column names and key formats slightly differ.

**Assumption 2**  
Instead of a live database, we assume the Excel files represent the “Source of Truth” (simulating an export from an older ERP system).

---

## In Scope

- Identifying whether the same defect type appears across multiple lots over time
- Distinguishing recurring defect issues from one-off incidents
- Aggregating inspection data across daily and weekly inspection logs
- Excluding non-defect inspection records (e.g., `Qty Defects = 0`) from defect occurrence counts
- Indicating when available data is insufficient to determine recurrence

---

## Out of Scope

- Root cause analysis of defects
- Predictive or AI-based quality analysis
- Real-time inspection or production monitoring
- Enforcement of data correctness at the source (e.g., preventing bad Excel entries)
- User authentication, authorization, or role-based access control
- The dashboard needs to be functional and clean, but not a “pixel-perfect” consumer-grade design
