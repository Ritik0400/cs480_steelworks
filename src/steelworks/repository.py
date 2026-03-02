"""Data access layer stubs.

The repository is responsible for fetching raw records from whatever storage
(backing DB, CSV, etc.).  For now it contains only method signatures matching
what the services layer will need.  Each method raises NotImplementedError so
tests can assert the stub exists without performing real I/O.
"""

from typing import List, Optional
from datetime import date

from .models import ProductionRecord, InspectionRecord, ShippingRecord


class Repository:
    """Simple repository with filtering methods used by operations analytics.

    Methods accept optional parameters so that higher layers can request
    date/line filtering per AC1 and AC2.  Results are typed lists of the model
    classes defined in models.py.
    """

    def get_production_records(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        production_line: Optional[str] = None,
    ) -> List[ProductionRecord]:
        """Return productions within the given constraints.

        Parameters are all optional to support flexible querying.  Concrete
        implementations will translate these arguments into SQL queries or
        file filters.
        """
        raise NotImplementedError

    def get_inspection_records(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        production_line: Optional[str] = None,
    ) -> List[InspectionRecord]:
        """Return inspection events subject to the same filters."""
        raise NotImplementedError

    def get_shipping_record_for_lot(self, lot_id: str) -> Optional[ShippingRecord]:
        """Find a shipping row for *exact* lot identifier (pre-normalization).

        The service layer will normalize the ID before calling this method as
        part of implementing AC5/AC6.  Returning `None` signifies that no
        shipment record exists yet.
        """
        raise NotImplementedError
