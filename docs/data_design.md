# Operations Data Design (Logical)

This document extracts the **data entities** and **relationships** needed to support the Operations user story and acceptance criteria (filtering by date range/line, summary of issues by line, defect trends over time, and shipment status by lot).

---

## Entities

### Lots
Represents a manufacturing lot/batch that is referenced across production, inspection, and shipping.

**Attributes**
- lot_id (business identifier; may be formatted inconsistently across sources)

---

### Production_Lines
Represents a production line used for filtering and grouping.

**Attributes**
- production_line

---

### Production_Records
Represents production activity for a lot on a given date and production line.

**Attributes**
- production_date
- production_line
- lot_id

---

### Inspection_Records
Represents an inspection finding for a lot on a given date, including defect information.

**Attributes**
- inspection_date
- defect_code
- qty_defects
- lot_id

---

### Defects
Represents a defect type/category.

**Attributes**
- defect_code

---

### Shipping_Records
Represents shipment information for a lot (whether shipped and when).

**Attributes**
- ship_date
- ship_status
- lot_id

---

## Relationships

- One **Lot** can have many **Production_Records**
- One **Lot** can have many **Inspection_Records**
- One **Lot** can have many **Shipping_Records** (or 0/1 depending on source; model allows multiple shipments if needed)
- One **Defect** can appear in many **Inspection_Records**
- One **Production_Line** can have many **Production_Records**
- Each **Production_Record** references exactly one **Lot** and one **Production_Line**
- Each **Inspection_Record** references exactly one **Lot** and one **Defect**
- Each **Shipping_Record** references exactly one **Lot**

---

## ERD (Mermaid)

```mermaid
erDiagram
    LOTS ||--o{ PRODUCTION_RECORDS : has
    LOTS ||--o{ INSPECTION_RECORDS : has
    LOTS ||--o{ SHIPPING_RECORDS : has
    DEFECTS ||--o{ INSPECTION_RECORDS : appears_in
    PRODUCTION_LINES ||--o{ PRODUCTION_RECORDS : runs

    LOTS {
        string lot_id
    }

    PRODUCTION_LINES {
        string production_line
    }

    PRODUCTION_RECORDS {
        date production_date
        string production_line
        string lot_id
    }

    INSPECTION_RECORDS {
        date inspection_date
        string defect_code
        int qty_defects
        string lot_id
    }

    DEFECTS {
        string defect_code
    }

    SHIPPING_RECORDS {
        date ship_date
        string ship_status
        string lot_id
    }
