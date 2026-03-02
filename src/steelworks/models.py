"""Domain models representing rows in the various CSV/DB tables.

These classes are intentionally simple data holders (similar to "structs").
They are used by the repository layer to type its return values.  No
business logic belongs here; methods should be added only when necessary for
object behavior.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ProductionRecord:
    """A single production event according to the schema (see db/schema.sql).

    Fields correspond roughly to the columns in the raw spreadsheet:
    * id: primary key placeholder
    * lot_id: identifier for the batch/lot produced
    * production_line: which line produced the lot (used in AC2/AC3)
    * produced_at: date of production (used in AC1 date filtering)
    * quantity: number of items produced
    """

    id: int
    lot_id: str
    production_line: str
    produced_at: date
    quantity: int


@dataclass
class InspectionRecord:
    """Represents one inspection row, including optional defects.

    The user story refers to defect codes and quantities, so those fields are
    included as optionals.  Fields again mirror the spreadsheet layout.
    """

    id: int
    lot_id: str
    inspection_date: date
    production_line: str
    defect_code: Optional[str]
    defect_quantity: Optional[int]


@dataclass
class ShippingRecord:
    """Tracks shipping status for a lot.

    AC5 asks whether a lot has shipped; this record holds the status/date.
    """

    id: int
    lot_id: str
    shipped_at: Optional[date]
    status: str  # e.g. "shipped", "pending", etc.
