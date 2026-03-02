BEGIN;

-- Drop tables in dependency order (safe reruns)
DROP TABLE IF EXISTS shipping_records;
DROP TABLE IF EXISTS inspection_records;
DROP TABLE IF EXISTS production_records;
DROP TABLE IF EXISTS defects;
DROP TABLE IF EXISTS production_lines;
DROP TABLE IF EXISTS lots;

-- =========================
-- LOTS
-- =========================
CREATE TABLE lots (
    id BIGSERIAL PRIMARY KEY,
    lot TEXT NOT NULL UNIQUE
);

-- =========================
-- PRODUCTION LINES
-- =========================
CREATE TABLE production_lines (
    id BIGSERIAL PRIMARY KEY,
    line TEXT NOT NULL UNIQUE
);

-- =========================
-- DEFECT TYPES
-- =========================
CREATE TABLE defects (
    id BIGSERIAL PRIMARY KEY,
    defect_code TEXT NOT NULL UNIQUE
);

-- =========================
-- PRODUCTION RECORDS
-- =========================
CREATE TABLE production_records (
    id BIGSERIAL PRIMARY KEY,

    lot_id BIGINT NOT NULL,
    production_line_id BIGINT NOT NULL,

    date DATE NOT NULL,
    shift TEXT NOT NULL,
    part_number TEXT NOT NULL,

    units_planned INTEGER NOT NULL CHECK (units_planned >= 0),
    units_actual INTEGER NOT NULL CHECK (units_actual >= 0),
    downtime_min INTEGER NOT NULL CHECK (downtime_min >= 0),

    line_issue BOOLEAN NOT NULL,
    primary_issue TEXT NULL,
    supervisor_notes TEXT NULL,

    CONSTRAINT fk_production_lot
        FOREIGN KEY (lot_id)
        REFERENCES lots(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_production_line
        FOREIGN KEY (production_line_id)
        REFERENCES production_lines(id)
        ON DELETE RESTRICT
);

-- =========================
-- INSPECTION RECORDS
-- =========================
CREATE TABLE inspection_records (
    id BIGSERIAL PRIMARY KEY,

    lot_id BIGINT NOT NULL,
    production_line_id BIGINT NOT NULL,

    inspection_date DATE NOT NULL,
    inspection_time TIME NULL,

    inspector TEXT NOT NULL,
    part_number TEXT NOT NULL,

    defect_id BIGINT NULL,
    defect_description TEXT NULL,
    severity TEXT NULL,

    qty_checked INTEGER NOT NULL CHECK (qty_checked >= 0),
    qty_defects INTEGER NOT NULL CHECK (qty_defects >= 0),

    disposition TEXT NULL,
    notes TEXT NULL,

    CONSTRAINT fk_inspection_lot
        FOREIGN KEY (lot_id)
        REFERENCES lots(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_inspection_line
        FOREIGN KEY (production_line_id)
        REFERENCES production_lines(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_inspection_defect
        FOREIGN KEY (defect_id)
        REFERENCES defects(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_defect_presence
        CHECK (
            (qty_defects = 0 AND defect_id IS NULL)
            OR
            (qty_defects > 0 AND defect_id IS NOT NULL)
        )
);

-- =========================
-- SHIPPING RECORDS
-- =========================
CREATE TABLE shipping_records (
    id BIGSERIAL PRIMARY KEY,

    lot_id BIGINT NOT NULL,

    ship_date DATE NOT NULL,
    sales_order_no TEXT NOT NULL,
    customer TEXT NOT NULL,
    destination_state CHAR(2) NOT NULL,

    carrier TEXT NOT NULL,
    bol_no TEXT NOT NULL UNIQUE,
    tracking_pro TEXT NULL,

    qty_shipped INTEGER NOT NULL CHECK (qty_shipped >= 0),

    ship_status TEXT NOT NULL,
    hold_reason TEXT NULL,
    shipping_notes TEXT NULL,

    CONSTRAINT fk_shipping_lot
        FOREIGN KEY (lot_id)
        REFERENCES lots(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_ship_status
        CHECK (ship_status IN ('Shipped','Partial','On Hold','Cancelled','Pending'))
);

-- =========================
-- INDEXES (for queries)
-- =========================
CREATE INDEX idx_prod_date ON production_records(date);
CREATE INDEX idx_prod_line_date ON production_records(production_line_id, date);
CREATE INDEX idx_prod_lot ON production_records(lot_id);

CREATE INDEX idx_insp_date ON inspection_records(inspection_date);
CREATE INDEX idx_insp_defect_date ON inspection_records(defect_id, inspection_date);
CREATE INDEX idx_insp_lot ON inspection_records(lot_id);

CREATE INDEX idx_ship_date ON shipping_records(ship_date);
CREATE INDEX idx_ship_lot ON shipping_records(lot_id);
CREATE INDEX idx_ship_status ON shipping_records(ship_status);

COMMIT;
