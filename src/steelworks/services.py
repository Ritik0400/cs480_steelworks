"""Business logic layer for operations reporting.

This module contains classes whose methods correspond directly to the
acceptance criteria listed in the user story.  Methods are currently
unimplemented; they exist so that unit tests can be written against their
signatures.  Detailed docstrings explain intent and expected inputs/outputs.
"""

from typing import List, Any, Optional
from datetime import date

from .repository import Repository


class OperationsService:
    """Core service that produces analytics summaries.

    A real implementation would combine data from production,
    inspection and shipping records, apply filters, and compute aggregates.
    Each public method below maps to one or more ACs from the user story.
    """

    def __init__(self, repository: Repository):
        # repository is injected to allow easy mocking in tests
        self.repository = repository

    def summarize_issues_by_line(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Any]:
        """AC3: return lines sorted by total defects in a date range.

        The exact return type is a list of tuples or dictionaries; details are
        unimportant for the stub.  Filters are passed through to the
        repository.
        """
        raise NotImplementedError

    def defect_trends(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Any:
        """AC4: defect counts grouped by week for a date range.

        This would typically return a time series structure that can be
        plotted or iterated over.
        """
        raise NotImplementedError

    def check_lot_shipped(self, lot_id: str) -> Any:
        """AC5 & AC6: return shipment status and date for the normalized lot.

        The service is responsible for calling the normalize_lot_id helper
        before querying the repository.  It may return a tuple like
        `(shipped: bool, date: Optional[date])`.
        """
        raise NotImplementedError
