-- db/sample_queries.sql
-- Sample queries for Operations analytics (PostgreSQL)

-- =========================================================
-- Q1) Filter production by date range (AC1)
-- =========================================================
SELECT
    pr.date,
    pl.line,
    pr.shift,
    l.lot,
    pr.part_number,
    pr.units_planned,
    pr.units_actual,
    pr.downtime_min,
    pr.line_issue,
    pr.primary_issue
FROM production_records pr
JOIN lots l ON l.id = pr.lot_id
JOIN production_lines pl ON pl.id = pr.production_line_id
WHERE pr.date BETWEEN DATE '2026-01-01' AND DATE '2026-01-31'
ORDER BY pr.date, pl.line, l.lot;

-- =========================================================
-- Q2) Filter production by production line (AC2)
-- =========================================================
SELECT
    pr.date,
    pl.line,
    l.lot,
    pr.part_number,
    pr.units_actual,
    pr.downtime_min
FROM production_records pr
JOIN lots l ON l.id = pr.lot_id
JOIN production_lines pl ON pl.id = pr.production_line_id
WHERE pl.line = 'Line A'
ORDER BY pr.date, l.lot;

-- =========================================================
-- Q3) Which production lines had the most issues? (AC3)
-- Using inspection_records as "issues" when qty_defects > 0
-- =========================================================
SELECT
    pl.line,
    SUM(ir.qty_defects) AS total_defects,
    COUNT(*) FILTER (WHERE ir.qty_defects > 0) AS defect_rows
FROM inspection_records ir
JOIN production_lines pl ON pl.id = ir.production_line_id
WHERE ir.inspection_date BETWEEN DATE '2026-01-01' AND DATE '2026-01-31'
GROUP BY pl.line
ORDER BY total_defects DESC, defect_rows DESC;

-- =========================================================
-- Q4) Trending defect types by week (AC4)
-- (Postgres date_trunc('week', ...) gives week buckets
-- =========================================================
SELECT
    date_trunc('week', ir.inspection_date)::date AS week_start,
    d.defect_code,
    SUM(ir.qty_defects) AS total_defects
FROM inspection_records ir
JOIN defects d ON d.id = ir.defect_id
WHERE ir.inspection_date BETWEEN DATE '2026-01-01' AND DATE '2026-03-31'
  AND ir.qty_defects > 0
GROUP BY week_start, d.defect_code
ORDER BY week_start, total_defects DESC;

-- =========================================================
-- Q5) Has a lot shipped? (AC5)
-- If any record exists in shipping_records, it has shipped/has a status.
-- =========================================================
SELECT
    l.lot,
    sr.ship_status,
    sr.ship_date,
    sr.customer,
    sr.bol_no,
    sr.qty_shipped
FROM lots l
LEFT JOIN shipping_records sr ON sr.lot_id = l.id
WHERE l.lot = 'LOT-10025'
ORDER BY sr.ship_date DESC;

-- =========================================================
-- Q6) For a given lot, show production + shipping together (useful ops view)
-- =========================================================
SELECT
    l.lot,
    MIN(pr.date) AS first_production_date,
    MAX(pr.date) AS last_production_date,
    pl.line,
    SUM(pr.units_actual) AS total_units_actual,
    MAX(sr.ship_date) AS ship_date,
    MAX(sr.ship_status) AS ship_status
FROM lots l
JOIN production_records pr ON pr.lot_id = l.id
JOIN production_lines pl ON pl.id = pr.production_line_id
LEFT JOIN shipping_records sr ON sr.lot_id = l.id
WHERE l.lot = 'LOT-10025'
GROUP BY l.lot, pl.line;

-- =========================================================
-- Q7) Find lots with defects that have already shipped (ops question)
-- =========================================================
SELECT
    l.lot,
    pl.line,
    SUM(ir.qty_defects) AS total_defects,
    MAX(sr.ship_date) AS ship_date,
    MAX(sr.ship_status) AS ship_status
FROM inspection_records ir
JOIN lots l ON l.id = ir.lot_id
JOIN production_lines pl ON pl.id = ir.production_line_id
LEFT JOIN shipping_records sr ON sr.lot_id = l.id
WHERE ir.qty_defects > 0
GROUP BY l.lot, pl.line
HAVING MAX(sr.ship_date) IS NOT NULL
ORDER BY total_defects DESC;

-- =========================================================
-- Q8) Line downtime summary by week (ops reporting)
-- =========================================================
SELECT
    date_trunc('week', pr.date)::date AS week_start,
    pl.line,
    SUM(pr.downtime_min) AS total_downtime_min
FROM production_records pr
JOIN production_lines pl ON pl.id = pr.production_line_id
WHERE pr.date BETWEEN DATE '2026-01-01' AND DATE '2026-03-31'
GROUP BY week_start, pl.line
ORDER BY week_start, total_downtime_min DESC;
